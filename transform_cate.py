import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from sklearn import preprocessing
df=pd.read_csv("train.csv")


x=list(df["Category"].unique())
le = preprocessing.LabelEncoder()
le.fit(x)
y=list(le.transform(x))
y=list(map(lambda x:x+1,y))
z=zip(x,y)
d1=dict(list(z))
fp3=open("../mappings/Catmap.txt","w")
fp3.write(str(d1))


x=list(df["Address"].unique())
le = preprocessing.LabelEncoder()
le.fit(x)
y=list(le.transform(x))
y=list(map(lambda x:x+1,y))
z=zip(x,y)
d1=dict(list(z))
fp3=open("../mappings/addmapp.txt","w")
fp3.write(str(d1))


x=list(df["DayOfWeek"].unique())
le = preprocessing.LabelEncoder()
le.fit(x)
y=list(le.transform(x))
y=list(map(lambda x:x+1,y))
z=zip(x,y)
d1=dict(list(z))
fp3=open("../mappings/dowmapp.txt","w")
fp3.write(str(d1))


x=list(df["PdDistrict"].unique())
le = preprocessing.LabelEncoder()
le.fit(x)
y=list(le.transform(x))
y=list(map(lambda x:x+1,y))
z=zip(x,y)
d1=dict(list(z))
fp3=open("../mappings/pdmapp.txt","w")
fp3.write(str(d1))

