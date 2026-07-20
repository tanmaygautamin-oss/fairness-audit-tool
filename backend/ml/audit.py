"""
    ml/audit.py
        WHAT: Uses Fairlearn to measure whether the trained model treats different
            demographic groups fairly, and returns a structured report.
"""



from fairlearn.metrics import (
    MetricFrame, selection_rate, demographic_parity_difference,
    demographic_parity_ratio, equalized_odds_difference
)
from sklearn.metrics import accuracy_score, recall_score

def run_fairness_audit(model, X_test, y_test, sensitive_series):
    """
        WHAT this returns: per-group breakdown of key metrics, PLUS single-number
            overall fairness scores that summarize how big the gap is between groups.
        RETURNS: dict with keys:"""
    y_pred = model.predict(X_test)

    # MetricFrame computes a metric separately for EACH group automatically.
    metric_frame = MetricFrame(
        metrics={
            "accuracy": accuracy_score,
            "selection_rate": selection_rate, # % of people the model approves
            "true_positive_rate": recall_score # % of deserving people correctly approved
        },
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive_series
    )

    per_group_results = metric_frame.by_group.to_dict()

    overall_fairness = {
        "demographic_parity_difference": demographic_parity_difference(
            y_test, y_pred, sensitive_features=sensitive_series
        ),
        "demographic_parity_ratio": demographic_parity_ratio(
            y_test, y_pred, sensitive_features=sensitive_series
        ),
        "equalized_odds_difference": equalized_odds_difference(
            y_test, y_pred, sensitive_features=sensitive_series
        ),
        "overall_accuracy": accuracy_score(y_test, y_pred)
    }

    return {
        "per_group": per_group_results,
        "overall_fairness": overall_fairness,
        "flags": generate_flags(overall_fairness)
    }

def generate_flags(overall_fairness):
    """
        WHAT: Translates raw numbers into plain-language warnings -- this is
            what makes the tool genuinely USEFUL, not just a table of numbers.
    """

    flags = []
    if overall_fairness["demographic_parity_ratio"] < 0.8:
        flags.append("Demographic parity ratio < 0.8: model may be biased against some groups.")
    if overall_fairness["demographic_parity_difference"] > 0.1:
        flags.append("Demographic parity difference > 0.1: model may be biased against some groups.")
    
    if overall_fairness["equalized_odds_difference"] > 0.1:
        flags.append("Equalized odds difference > 0.1: model may be biased against some groups.")
    
    if not flags:
        flags.append("✅ No major fairness red flags detected at standard thresholds.")
    return flags





