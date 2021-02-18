from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Jason Eisele",
    "email": "jeisele@shipt.com",
}

dag = DAG(
    dag_id="example_ml_retrain",
    description="A simple ML retrain DAG",
    default_args=default_args,
    start_date=days_ago(2),
    # schedule_interval=timedelta(days=1),
    # on_success_callback=some_function(),
    # on_failure_callback=some_other_function(),
)

t1 = BashOperator(
    task_id="data_extraction",
    bash_command="echo I pulled some data!",
    dag=dag
)

t2 = BashOperator(
    task_id="data_validation",
    bash_command="echo I validated some data!",
    dag=dag
)

t3 = BashOperator(
    task_id="data_preparation",
    bash_command="echo I prepared some data!",
    dag=dag
)

t4 = BashOperator(
    task_id="model_training",
    bash_command="echo I trained an ML model!",
    dag=dag
)

t5 = BashOperator(
    task_id="model_evaluation",
    bash_command="echo I evaluated my ML model, lets validate on unseen data!",
    dag=dag
)

t6 = BashOperator(
    task_id="model_validation",
    bash_command="echo I validated my ML model, looks good!",
    dag=dag
)

t1 >> t2 >> t3 >> t4 >> t5 >> t6
