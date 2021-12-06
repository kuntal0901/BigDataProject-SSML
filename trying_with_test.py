import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row, SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,StringType
from pyspark.sql.functions import *
from pyspark.ml.feature import StringIndexer
import ast
import model

Model=model.makeModel()

flag=True

sc = SparkContext("local[2]", "crime_data")	
fp=open('mappings/addmapp.txt','r')
fp1=open("mappings/pdmapp.txt","r")
fp2=open("mappings/dowmapp.txt","r")
fp3=open("mappings/Catmap.txt","r")
addressmappings=ast.literal_eval(fp.read())
dayofweekmappings=ast.literal_eval(fp2.read())
pddistrictmappings=ast.literal_eval(fp1.read())
categorymappings=ast.literal_eval(fp3.read())
spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()
ssc = StreamingContext(sc, 1)
sql_context = SQLContext(sc)
schema2 = StructType([
    StructField("ID", StringType(), False),
	StructField("Dates", StringType(), False),
    StructField("DayOfWeek", StringType(), False),
    StructField("PdDistrict", StringType(), False),
    StructField("Address", StringType(), False),
    StructField("X", StringType(), False),
    StructField("Y", StringType(), False)
])
schema3 = StructType([
	 StructField("DayOfWeek", StringType(), False),
    StructField("PdDistrict", StringType(), False),
    StructField("Address", StringType(), False),
    StructField("X", StringType(), False),
    StructField("Y", StringType(), False),
    StructField("Year", StringType(), False),
    StructField("Month", StringType(), False),
    StructField("Date", StringType(), False),
    StructField("Hour", StringType(), False),
    StructField("Minute", StringType(), False)    
])
def preprocessing(df):
   df = df.withColumn('year',year(df.Dates))
   df = df.withColumn('month',month(df.Dates))
   df = df.withColumn('date',dayofmonth(df.Dates))
   df = df.withColumn('hour',hour(df.Dates))
   df = df.withColumn('minute',minute(df.Dates))
   df=df.drop("Descript","Resolution","Dates","ID")
   df_X_train=df      
   rdd=df_X_train.rdd.map(lambda x: (dayofweekmappings[x["DayOfWeek"]],pddistrictmappings[x["PdDistrict"]],addressmappings[x["Address"]],x["X"],x["Y"],x["year"],x["month"],x["date"],x["hour"],x["minute"]))
   df_X_final=spark.createDataFrame(data=rdd,schema=schema3)
   df_X_final.show() 
   
def convert_to_df(rdd):
	global schema, spark
	records = rdd.collect()
	dicts = [i for j in records for i in list(json.loads(j).values())]
	if len(dicts) == 0:
		return		
	df = spark.createDataFrame((Row(**d) for d in dicts), schema2)
	preprocessing(df)
lines = ssc.socketTextStream("localhost",6100)
json_str = lines.flatMap(lambda x: x.split('\n'))
lines.foreachRDD(convert_to_df)
ssc.start()
ssc.awaitTermination()
