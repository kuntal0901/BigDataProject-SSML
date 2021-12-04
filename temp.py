from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)
data=[]
for i in range(1000):
    x=i
    y=i**2
    z=x+y
    data.append((x,y,z))
schema = StructType([StructField("a",StringType(),True),StructField("b",StringType(),True),StructField("c",StringType(),True)])
df = spark.createDataFrame(data=data,schema=schema)
df.show()