
import joblib
from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier as mo
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.model_selection import train_test_split
from sklearn import metrics 
import pickle



def load_model():
    print("Loading model from directory.............................................................")
    mod=joblib.load('model.joblib')
    return mod

def store_model(mod):
    print("Storing model............................................................................")
    joblib.dump(mod,'model.joblib')



def makeModel():
    mod=mo()
    return mod

def ifit(mod,X,Y,des=None):
    X=X.toPandas()
    Y=Y.toPandas().values.ravel()
    try:
        if(des is not None):
            mod.partial_fit(X,Y,classes=des)
        else:
            
            mod.partial_fit(X,Y)
    except ValueError as e:
        print(e)


def test(mod,x,Y,accli):
    print("Predicting ...............................................................................")
    x=x.toPandas()
    y=mod.predict(x)
    Y=Y.toPandas()
    accli.append(metrics.accuracy_score(Y,y))
