from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
from random import randint

def random():
    return randint(1, 10)


with DAG(
    "test_dag", # Dag id
    start_date=datetime(2021, 1 ,1), # start date, the 1st of January 2021 
    schedule_interval='@daily',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
    catchup=False  # Catchup 
) as dag :
    test_1 = PythonOperator(
        task_id="test_1",
        python_callable=random
    )


