from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
            SparkSession.builder.appName("BigLake Metastore Iceberg")
            .master("local[*]")
            .config("spark.jars.packages","com.google.cloud.spark:spark-3.5-bigquery:0.42.2")
            .config("spark.jars", "gcs-connector-hadoop3-2.2.28-shaded.jar,iceberg-spark-runtime-3.5_2.13-1.10.0-20250724.003223-61.jar,iceberg-bigquery-catalog-1.6.1-1.0.1-beta.jar")
            .config("spark.eventLog.dir", "gs://cf-phs/spark-job-history")
            .config("spark.eventLog.enabled", "true")
            .config("spark.hadoop.google.cloud.auth.type", "SERVICE_ACCOUNT_JSON_KEYFILE")
            .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "cf-data-analytics-4f457ddf908d.json" )
            .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
            .config("spark.sql.catalog.bl_catalog.gcp_project", "cf-data-analytics")
            .config("spark.sql.catalog.bl_catalog.type", "bigquery")
            .config("spark.sql.catalog.bl_catalog", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.bl_catalog.gcp_location", "us-central1")
            .config("spark.sql.catalog.bl_catalog.warehouse", "gs://cf-data-temp/")
            .getOrCreate()
        )

spark.conf.set("viewsEnabled","true")


df = (
    spark.read
    .format("bigquery")
    .option("table", "cf-data-analytics.iceberg.wiki_nc")
    .load()
    .filter(F.to_date(F.col("datehour")) == "2024-07-09")
)

# distinct_title_count = df.select("title").distinct().count()
# print(distinct_title_count)

spark.sql("USE `bl_catalog`;")
spark.sql("USE NAMESPACE iceberg;")

df.show()

df.sh()


df = spark.sql("SHOW TABLES;")
df.show();
