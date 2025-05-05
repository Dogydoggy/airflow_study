from airflow import DAG
from datetime import datetime, timedelta
from airflow.decorators import task
from utils.utils import query_dml_db,copy_csv_db
import logging

with DAG(
    dag_id="cn_update",
    default_args={
        'owner': 'airflow',  # DAG 소유자
        'start_date': datetime(2025, 5, 3),  # 시작일
        'retries': 1,  # 실패 시 재시도 횟수
        'retry_delay': timedelta(minutes=2),  # 재시도 간격
    },
    schedule_interval=timedelta(minutes=5),  # 5분마다 실행
    catchup=False,  # 누락된 DAG 실행을 피하려면 False로 설정
    tags=['example'],  # 태그 설정
) as dag:
    
    @task
    def trunc():
        logging.info("trunc task started")
        with open('/opt/airflow/sql/template/truncate.sql', 'r') as sql_file:
            logging.info("trunc sql file reading..")
            sql = sql_file.read()
            logging.info("sql file read succeeded.")
        sql = sql.format(table_name='company_info')
        query_dml_db('cn',sql)
        logging.info("truncate done")

    @task
    def copy():
        with open('/opt/airflow/sql/csv_company_info.sql', 'r') as sql_file:
            sql = sql_file.read()
        csv_path = '/opt/airflow/data/cn_company.csv'
        copy_csv_db('cn',sql,csv_path)
    
    trunc() >> copy()