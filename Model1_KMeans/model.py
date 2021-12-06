
import joblib
from sklearn import preprocessing
from sklearn.cluster import MiniBatchKMeans as mo
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.model_selection import train_test_split
import pickle

def load_model():
    print("Loading model from directory.............................................................")
    mod=joblib.load('model.joblib')
    return mod

def store_model(mod):
    print("Storing model............................................................................")
    joblib.dump(mod,'model.joblib')

def store_transform(mappings):
    with open('transform.pkl','wb') as f:
        pickle.dump(mappings,f)

def get_transform():
    with open('transform.pkl','rb') as f:
        mappings=pickle.load(f)
    return mappings

def makeModel():
    mod=mo()
    return mod

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

def ifit(mod,X,Y,des=None):
    X=X.toPandas()
    try:
        mod.partial_fit(X)
    except ValueError as e:
        print(e)


def test(mod,x):
    print("Predicting ...............................................................................")
    x=x.toPandas()
    y=mod.predict(x)
    y1=list(map(lambda x:(str(x),),y))
    return y1
