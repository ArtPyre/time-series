from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, exc
import lib_helper.tickers_scrapper as ts
import lib_helper.stock_scrapper as sts


def scrap_daily(**context) :
    start_time = context['yesterday_ds']
    end_time = context['ds']
    engine = create_engine('sqlite:///dags/lib_helper/stocks.db')

    try:
        df_tickers = pd.read_sql('stocks', engine)
    except (exc.OperationalError) :
        ts.get_tickers()
        df_tickers = pd.read_sql('stocks', engine)

    tickers = df_tickers.values
    for t in tickers :
        sts.stock_to_df(t[0], start_time, end_time)

default_args = {
    'owner' : 'Arthur',
    'retries' : 5,
    'retry_delay' : timedelta(minutes=10),
}

with DAG(
    dag_id="scrapper_dag_V2",
    description="A dag that refresh all the tickers' datas from this day",
    default_args=default_args,
    start_date=datetime(2023, 3 ,15),
    schedule_interval='@daily'
) as dag :
    refresh_all_tickers = PythonOperator(
        task_id="scrap_daily",
        python_callable=scrap_daily,
        provide_context=True
    )
