from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import sys
import os

sys.path.insert(0, '/opt/airflow')

from scripts.section1.main import main

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'tiktok_pipeline',
    default_args=default_args,
    description='TikTok data pipeline',
    schedule_interval=timedelta(days=1),
)

def run_pipeline(**kwargs):
    json_path = Variable.get("JSON_DATA", default_var=None)
    database_url = Variable.get("DATABASE_URL", default_var=None)
    
    return main(json_path, database_url)

run_pipeline_task = PythonOperator(
    task_id='run_tiktok_pipeline',
    python_callable=run_pipeline,
    provide_context=True,
    dag=dag,
)