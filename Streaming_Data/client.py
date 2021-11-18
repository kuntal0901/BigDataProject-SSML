import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row, SparkSession
from pyspark.sql.types import StructType,StructField,StringType
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
def process(rdd):
	global schema, spark
	records = rdd.collect()
	dicts = [i for j in records for i in list(json.loads(j).values())]
	if len(dicts) == 0:
		return		
	df = spark.createDataFrame((Row(**d) for d in dicts), schema)
	df.show()
lines = ssc.socketTextStream("localhost",6100)
json_str = lines.flatMap(lambda x: x.split('\n'))
lines.foreachRDD(process)
ssc.start()
ssc.awaitTermination()
