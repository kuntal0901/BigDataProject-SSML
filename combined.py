import joblib
from sklearn import preprocessing
from sklearn.naive_bayes import BernoulliNB as Ber
from sklearn.linear_model import PassiveAggressiveClassifier as PAG
from sklearn.linear_model import SGDClassifier as SGD
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

def load_model():
    print("Loading model from directory.............................................................")
    models=[]
    models.append(joblib.load('Bernoulli.joblib'))
    models.append(joblib.load('PassiveAggressive.joblib'))
    models.append(joblib.load('SGD.joblib'))
    return models

def store_model(models):
    print("Storing model............................................................................")
    joblib.dump(models[0],'Bernoulli.jobllib')
    joblib.dump(models[1],'PassiveAggressive.jobllib')
    joblib.dump(models[2],'SGD.jobllib')

def store_transform(mappings):
    with open('transform.pkl','wb') as f:
        pickle.dump(mappings,f)

def get_transform():
    with open('transform.pkl','rb') as f:
        mappings=pickle.load(f)
    return mappings

def makeModel():
    models=[Ber(),PAG(),SGD()]
    return models

def make_transform(df):
    col=['DayOfWeek','PdDistrict','Address']
    mappings={}
    for i in col:
        label=preprocessing.LabelEncoder()
        label.fit(df[i])
        mappings[i]=dict(zip(label.classes_, label.transform(label.classes_)))
    store_transform(mappings)
    return mappings

def transform(df):
    mappings=get_transform()
    col=['DayOfWeek','PdDistrict','Address']
    for i in col:
        df[i]=df[i].map(mappings[i])

def ifit(models,X,Y,des=None):
    X=X.toPandas()
    Y=Y.toPandas().values.ravel()
    for mod in models:
        try:
            if(des is not None):
                mod.partial_fit(X,Y,classes=des)
            else:
                
                mod.partial_fit(X,Y)
        except ValueError as e:
            print(e)


def test(models,x,Y=None,accli=None):
    print("Predicting ...............................................................................")
    x=x.toPandas()
    out=[]
    for i in range(len(models)):
        y=models[i].predict(x)
        y1=list(map(lambda x:(str(x),),y))
        out.append(y1)
        if Y is not None:
            Y=Y.toPandas()
            accli[i].append(metrics.accuracy_score(Y,y))
    return out
