from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from harness.th_model_classes.class_sklearn_classification import SklearnClassification

features = ['_rxn_M_acid',
 '_rxn_M_inorganic',
 '_rxn_M_organic',
 '_rxn_mixingtime1S',
 '_rxn_mixingtime2S',
 '_rxn_reactiontimeS',
 '_rxn_stirrateRPM',
]

class RxnOnlySVM(SklearnClassification):
    def __init__(self):
        self.features = features
        self.svm = SVC(kernel='rbf',
                       decision_function_shape='ovr',
                       probability=True,
                       C=0.1,
        )

    def fit(self,X,y):
        self.svm.fit(X[self.features],y)

    def predict(self,X):
        return self.svm.predict(X[self.features])
    
    def predict_proba(self,X):
        return self.svm.predict_proba(X[self.features])
    
def rxn_only_svm():
    model = RxnOnlySVM()
    return SklearnClassification(model=model,
                                     model_author="Scott Novotney",
                                     model_description="RBF svm w/only rxn features",
    )




class RxnOnlyXGB(SklearnClassification):
    def __init__(self):
        self.features = features
        self.xgb = GradientBoostingClassifier(
            learning_rate=2,
            max_depth=3,
            n_estimators=10
        )

    def fit(self,X,y):
        self.xgb.fit(X[self.features],y)

    def predict(self,X):
        return self.xgb.predict(X[self.features])
    
    def predict_proba(self,X):
        return self.xgb.predict_proba(X[self.features])
    
def rxn_only_xgb():
    model = RxnOnlyXGB()
    return SklearnClassification(model=model,
                                     model_author="Scott Novotney",
                                     model_description="RBF xgb using only 3 rxn features",
    )
