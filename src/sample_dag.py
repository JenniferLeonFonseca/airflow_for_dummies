from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator


def get_sum_of_prices(**kwargs):
    start_date = kwargs['execution_date']
    end_date = start_date.add(months=1)
    print('GETTING DATA FROM %s TO %s' % (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

    
dag = DAG('get_report',
          description='Gets sum of all purchased items prices for the last month',
          schedule_interval='0 4 1 * *',
          start_date=datetime(2020, 9, 22), catchup=True)


dummy_operator = DummyOperator(task_id='start', retries=3, dag=dag)
etl_operator = PythonOperator(task_id='get_prices', python_callable=get_sum_of_prices,
                              dag=dag, provide_context=True)

dummy_operator >> etl_operator