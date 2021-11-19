import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row, SparkSession
from pyspark.sql.types import StructType,StructField,StringType
from pyspark.sql.functions import *
from pyspark.ml.feature import StringIndexer


sc = SparkContext("local[2]", "crime_data")
spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()
ssc = StreamingContext(sc, 1)
sql_context = SQLContext(sc)


schema = StructType([
StructField("Dates", StringType(), False),
StructField("Category", StringType(), False),
StructField("Descript", StringType(), False),
StructField("DayOfWeek", StringType(), False),
StructField("PdDistrict", StringType(), False),
StructField("Resolution", StringType(), False),
StructField("Address", StringType(), False),
StructField("X", StringType(), False),
StructField("Y", StringType(), False)

])

def preprocessing(df):
   df = df.withColumn('year',year(df.Dates))
   df = df.withColumn('month',month(df.Dates))
   df = df.withColumn('date',dayofmonth(df.Dates))
   df = df.withColumn('hour',hour(df.Dates))
   df = df.withColumn('minute',minute(df.Dates))
   df_Y_train=df.select("Category")
   df=df.drop("Descript","Resolution","Dates","Category")
   df_X_train=df
   df_X_train.show()
   #indexer = StringIndexer(inputCol="Category", outputCol="CategoryIndex")
   #df_Y_train = indexer.fit(df_Y_train).transform(df_Y_train)
   #df_Y_train.show()
   #rdd=df_Y_train.rdd

   #df.show()
   #pass

def convert_to_df(rdd):
   global schema, spark
   records = rdd.collect()
   dicts = [i for j in records for i in list(json.loads(j).values())]
   if len(dicts) == 0:
     return
   df = spark.createDataFrame((Row(**d) for d in dicts), schema)
   #df.show()
   preprocessing(df)
   
lines = ssc.socketTextStream("localhost",6100)
json_str = lines.flatMap(lambda x: x.split('\n'))
lines.foreachRDD(convert_to_df)
ssc.start()
ssc.awaitTermination()
