from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'keerthi',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def run_spark_job():
    result = subprocess.run(
        ['python', '/Users/keerthi/url-shortener/pipeline/spark/analytics_processor.py'],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Spark job failed: {result.stderr}")

with DAG(
    dag_id='url_analytics_pipeline',
    default_args=default_args,
    description='Runs URL analytics pipeline every hour',
    schedule_interval='@hourly',
    start_date=datetime(2026, 3, 24),
    catchup=False,
    tags=['url-shortener', 'analytics'],
) as dag:

    check_kafka = BashOperator(
        task_id='check_kafka_running',
        bash_command='docker ps | grep kafka && echo "Kafka is up" || echo "Kafka not running"',
    )

    run_analytics = PythonOperator(
        task_id='run_spark_analytics',
        python_callable=run_spark_job,
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /Users/keerthi/url-shortener && source venv/bin/activate && dbt run --project-dir pipeline/dbt/url_analytics',
    )

    check_kafka >> run_analytics >> run_dbt
