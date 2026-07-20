"""
    ml/mitigate.py
        WHAT: Applies post-processing bias mitigation using Fairlearn's
            ThresholdOptimizer, which picks a DIFFERENT decision threshold per
            group so the chosen fairness constraint is satisfied.
"""

from fairlearn.postprocessing import ThresholdOptimizer
from fairlearn.metrics import (
    demographic_parity_difference, demographic_parity_ratio,
    equalized_odds_difference
)
from sklearn.metrics import accuracy_score

def mitigate_bias(model, X_train, y_train, sens_train, X_test, y_test, sens_test):
    """
    WHY 'equalized_odds' as our constraint: it's the stricter, more
        commonly-recommended fairness definition for high-stakes decisions
        like income/loan prediction.
    """

    mitigator = ThresholdOptimizer(
        estimator=model,
        constraints="equalized_odds",
        predict_method="predict_proba",
        prefit=True
    )
    mitigator.fit(X_train, y_train, sensitive_features=sens_train)
    y_pred_mitigated = mitigator.predict(X_test, sensitive_features=sens_test)

    return {
        "mitigated_accuracy": accuracy_score(y_test, y_pred_mitigated),
        "mitigated_demographic_parity_difference": demographic_parity_difference(
            y_test, y_pred_mitigated, sensitive_features=sens_test
        ),
        "mitigated_demographic_parity_ratio": demographic_parity_ratio(
            y_test, y_pred_mitigated, sensitive_features=sens_test
        ),
        "mitigated_equalized_odds_difference": equalized_odds_difference(
            y_test, y_pred_mitigated, sensitive_features=sens_test
        )
    }



