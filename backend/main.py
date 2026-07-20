"""
    main.py
        WHAT: Exposes our fairness audit pipeline as a REST API the React frontend
            can call. Trains the model once at startup and caches it in memory.
        HOW TO RUN: uvicorn main:app --reload --port 8000
"""



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml.data import load_real_data
from ml.model import train_classifier, evaluate_accuracy
from ml.audit import run_fairness_audit
from ml.mitigate import mitigate_bias

app = FastAPI(title="Bias/Fairness Audit Tool API")

# STEP: Allow our React frontend (running on a different port) to call this API.
# WHY this matters: browsers block cross-origin requests by default for security --
# this explicitly whitelists our known frontend URL.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Train once at startup, keep in memory -- avoids retraining on every request.

print("Loading real data and training model at startup...")

X_train, X_test, y_train, y_test, sens_train, sens_test = load_real_data()
model = train_classifier(X_train, y_train)

print("Model ready.")

class AuditRequest(BaseModel):
    """
        WHAT: Defines the expected structure of the request body for the /audit endpoint.
        FIELDS:
            - sensitive_attribute: str, the name of the sensitive attribute to audit (e.g., "sex" or "race")
    """
    sensitive_attribute: str # "sex" or "race"

@app.get("/api/health")

def health_check():
    return {"status": "ok", "records_loaded": len(X_train) + len(X_test)}

@app.post("/api/audit")
def audit(request: AuditRequest):
    if request.sensitive_attribute not in sens_test.columns:
        raise HTTPException(status_code=400, detail=f"Invalid sensitive attribute: {request.sensitive_attribute}")
    
    sensitive_series = sens_test[request.sensitive_attribute]
    report = run_fairness_audit(model, X_test, y_test, sensitive_series)
    report["baseline_accuracy"] = evaluate_accuracy(model, X_test, y_test)

    return report

@app.post("/api/mitigate")
def mitigate(request: AuditRequest):
    if request.sensitive_attribute not in sens_test.columns:
        raise HTTPException(status_code=400, detail="Unknown sensitive attribute.")
    sens_train_col = sens_train[request.sensitive_attribute]
    sens_test_col = sens_test[request.sensitive_attribute]
    result = mitigate_bias(
        model, X_train, y_train, sens_train_col, X_test, y_test, sens_test_col
    )
    return result




