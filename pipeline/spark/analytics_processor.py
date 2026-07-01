from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, max as spark_max, min as spark_min

JDBC_URL = "jdbc:postgresql://localhost:5432/urlshortener"
JDBC_PROPERTIES = {
    "user": "urluser",
    "password": "urlpassword",
    "driver": "org.postgresql.Driver"
}

def create_spark_session():
    return SparkSession.builder \
        .appName("URLAnalyticsProcessor") \
        .config("spark.jars.packages",
                "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()

def run_analytics():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print("Reading click events from PostgreSQL...")

    clicks_df = spark.read \
        .jdbc(
            url=JDBC_URL,
            table="click_events",
            properties=JDBC_PROPERTIES
        )

    print(f"Total click events: {clicks_df.count()}")

    analytics_df = clicks_df \
        .groupBy("short_code", "original_url") \
        .agg(
            count("*").alias("total_clicks"),
            spark_min("timestamp").alias("first_click"),
            spark_max("timestamp").alias("last_click")
        ) \
        .orderBy(col("total_clicks").desc())

    print("\n--- URL Analytics Summary ---")
    analytics_df.show(truncate=False)

    analytics_df.write \
        .jdbc(
            url=JDBC_URL,
            table="url_analytics",
            mode="overwrite",
            properties=JDBC_PROPERTIES
        )

    print("Analytics written to url_analytics table")
    spark.stop()

if __name__ == "__main__":
    run_analytics()