"""
    ml/model.py
        WHAT: Trains a simple, explainable Logistic Regression classifier on the
            real data to predict whether income exceeds $50K.
"""



from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_classifier(X_train, y_train):

    """
        WHY Logistic Regression specifically: it's fast, and its predictions
         are easy to threshold per-group later during mitigation -- a more
         complex model would work too, but this keeps the demo clear.
        RETURNS: trained sklearn LogisticRegression model"""
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

def evaluate_accuracy(model, X_test, y_test):
    """
        WHAT: Evaluates the accuracy of a trained model on held-out test data.
        RETURNS: accuracy score (float)"""
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)


   
