from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WordCount") \
    .getOrCreate()

sc = spark.sparkContext

text = sc.textFile("input.txt")

word_counts = text \
    .flatMap(lambda line: line.split()) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)

for word, count in word_counts.collect():
    print(word, count)

spark.stop()