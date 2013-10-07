"""Key metrics for analysis of bubo applications"""
import sklearn.metrics
    
def average_precision(y_true, y_pred):
    """sklearn wrapper"""
    return sklearn.metrics.average_precision_score(y_true, y_pred)

def f1_score(y_true, y_pred):
    """sklearn wrapper"""    
    return sklearn.metrics.f1_score(y_true, y_pred)

def confusion_matrix(y_true, y_pred):
    return sklearn.metrics.confusion_matrix(y_true, y_pred)    

def categorization_report(Y_true, Y_pred, labels):
    return sklearn.metrics.classification_report(Y_true, Y_pred, target_names=labels)    

def precision_recall(y_true, y_pred):
    (precision, recall, thresholds) = sklearn.metrics.precision_recall_curve(y_true, y_pred)
    return (precision, recall)

