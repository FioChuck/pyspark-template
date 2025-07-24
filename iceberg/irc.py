
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

import google.auth
import google.auth.transport.requests


def get_simple_gcp_access_token():
    try:
        credentials, project = google.auth.default()
        if not credentials.valid and credentials.refresh_token:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
        return credentials.token
    except Exception as e:
        return None

access_token = get_simple_gcp_access_token()

spark = (
    SparkSession.builder.appName("BigLake Metastore Iceberg")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "com.google.cloud.spark:spark-3.5-bigquery:0.42.2"
    )
    .config("spark.jars", "gcs-connector-hadoop3-2.2.28-shaded.jar,iceberg-spark-runtime-3.5_2.13-1.9.2.jar, iceberg-bigquery-catalog-1.6.1-1.0.1-beta.jar")
    .config("spark.eventLog.dir", "gs://cf-phs/spark-job-history")
    .config("spark.eventLog.enabled", "true")
    .config("spark.hadoop.google.cloud.auth.type", "SERVICE_ACCOUNT_JSON_KEYFILE")
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "cf-data-analytics-4f457ddf908d.json" )
    .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    .config(f"spark.sql.catalog.bl_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config(f"spark.sql.catalog.bl_catalog.type", "rest")
    .config(f"spark.sql.catalog.bl_catalog.uri","https://biglake.googleapis.com/iceberg/v1beta/restcatalog")
    .config(f"spark.sql.catalog.bl_catalog.warehouse", "gs://cf-iceberg-in-bq")
    .config(f"spark.sql.catalog.bl_catalog.token", access_token)
    .config(f"spark.sql.catalog.bl_catalog.oauth2-server-uri", "https://oauth2.googleapis.com/token")
    .config(f"spark.sql.catalog.bl_catalog.header.x-goog-user-project", "cf-data-analytics")
    .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config(f"spark.sql.catalog.bl_catalog.io-impl","org.apache.iceberg.hadoop.HadoopFileIO")
    .config(f"spark.sql.catalog.bl_catalog.rest-metrics-reporting-enabled", "false")
    .getOrCreate()
)

spark.conf.set("viewsEnabled","true")

spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg;")
spark.sql("USE iceberg;")

spark.sql("SHOW TABLES").show()
