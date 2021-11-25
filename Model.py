import pandas as pd
import joblib
from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier as mo
from sklearn.model_selection import train_test_split
import pickle

def load_model():
    mod=joblib.load('model.joblib')
    return mod

def store_model(mod):
    joblib.dump(mod,'model.joblib')

def store_transform(mappings):
    with open('transform.pkl','wb') as f:
        pickle.dump(mappings,f)

def get_transform():
    with open('transform.pkl','rb') as f:
        mappings=pickle.load(f)
    return mappings

def unique_classes():
    df=pd.read_csv('train.csv')
    des=df['Category'].unique()
    with open('unique_classes.pkl','wb') as f:
        pickle.dump(des,f)
    with open('unique_classes.pkl','rb') as f:
        classes=pickle.load(f)
    return classes

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

def ifit(mod,df,des=None):
    transform(df)
    X=df.drop(['Dates','Category','Descript','Resolution'],axis=1)
    Y=df['Category']
    try:
        if(des is not None):
            mod.partial_fit(X,Y,classes=des)
        else:
            mod.partial_fit(X,Y)
    except ValueError as e:
        print(e)


def temp(mod):
    
    df=pd.read_csv('train.csv')
    X=df.drop(['Category','Descript','Resolution','Dates'],axis=1)
    Y=df['Category']
    x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.1)
    transform(x_test)
    score=mod.score(x_test,y_test)
    print(score)

def main():
    '''df=pd.read_csv('train.csv')
    make_transform(df)
    des=df['Category'].unique()'''

    df=pd.read_csv('train.csv',chunksize=8781)
    mod=makeModel()
    classes=unique_classes()
    count=0
    for i in df:
        print(count)
        if count==0:
            ifit(mod,i,classes)
        else:
            ifit(mod,i)
        count+=1
    store_model(mod)

if __name__=='__main__':
    main()
