import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row, SparkSession
from pyspark.sql.types import StructType,StructField,StringType

# Create a local StreamingContext with two execution threads
sc = SparkContext("local[2]", "Sentiment")
    
spark = SparkSession \
.builder \
.config(conf=SparkConf()) \
.getOrCreate()

# Batch interval of 5 seconds - TODO: Change according to necessity
ssc = StreamingContext(sc, 5)

sql_context = SQLContext(sc)
    
# Set constant for the TCP port to send from/listen to
TCP_IP = "localhost"
TCP_PORT = 6100
    
# Create schema
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

# Process each stream - needs to run ML models
def process(rdd):
    global schema, spark
    
    # Collect all records
    records = rdd.collect()
    
    # List of dicts
    dicts = [i for j in records for i in list(json.loads(j).values())]

    
    if len(dicts) == 0:
        return
        
    df = spark.createDataFrame((Row(**d) for d in dicts), schema)
    df.show()



# Main entry point for all streaming functionality
if __name__ == '__main__':

    # Create a DStream - represents the stream of data received from TCP source/data server
    # Each record in 'lines' is a line of text
    lines = ssc.socketTextStream(TCP_IP, TCP_PORT)

    # TODO: check if split is necessary
    json_str = lines.flatMap(lambda x: x.split('\n'))
    
    # Process each RDD
    lines.foreachRDD(process)

    # The data is streamed as a JSON string (you can see this by observing the code in stream.py). 
    # You will first need to parse the JSON string, obtain the rows in each batch and then convert it to a DataFrame. 
    # The structure of the JSON string has been provided in the streaming file. 
    # Use this to parse your JSON to obtain rows, and then convert these rows into a DataFrame.

    # Start processing after all the transformations have been setup
    ssc.start()             # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate
