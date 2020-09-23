from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import TaskInstance
from airflow.utils.db import provide_session
from airflow.utils.state import State

TASK_ID = 'sample_task_id'

dag = DAG('sample_dag', description='This is a sample DAG',
          start_date=datetime(2018, 11, 1),
          max_active_runs=1,
          schedule_interval='5 * * * *',
          catchup=False)


@provide_session
def get_last_task_run_date_time(session=None):
    latest_successful_task_instance = session.query(
        TaskInstance).filter(
        TaskInstance.state == State.SUCCESS).filter(
        TaskInstance.task_id == TASK_ID).order_by(
        TaskInstance.execution_date.desc()).first()

    latest_successful_task_date = latest_successful_task_instance.start_date \
        if latest_successful_task_instance is not None else None

    return latest_successful_task_date

def print_datetime(last_run_datetime):
    print('Last run at %s' % last_run_datetime if last_run_datetime else 'First run')

sample_task = PythonOperator(task_id=TASK_ID,
                             python_callable=print_datetime,
                             dag=dag,
                             op_args=[get_last_task_run_date_time()])