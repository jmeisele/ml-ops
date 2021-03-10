from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "Jason Eisele",
    "email": "jeisele@shipt.com",
}

dag = DAG(
    dag_id="python_example_ml_retrain",
    description="A simple ML retrain DAG using Python",
    default_args=default_args,
    start_date=days_ago(2),
    # schedule_interval=timedelta(days=1),
    # on_success_callback=some_function(),
    # on_failure_callback=some_other_function(),
)


def pull_data():
    data = "I pulled from data!"
    return data


def validate_data():
    valid_data = "Yep, looks good"
    return valid_data


def prep_data():
    prepped_data = "All clean and tidy"
    return prepped_data


def train_model():
    model = "This thing is powerful supposedly"
    return model


def evaluate_model():
    model_evaluated = "Looks great so far, let's check new data"
    return model_evaluated


def validate_model():
    model_validated = "Even performs great on new data"
    return model_validated


t1 = PythonOperator(
    task_id="data_extraction",
    python_callable=pull_data,
    dag=dag
)

t2 = PythonOperator(
    task_id="data_validation",
    python_callable=validate_data,
    dag=dag
)

t3 = PythonOperator(
    task_id="data_preparation",
    python_callable=prep_data,
    dag=dag
)

t4 = PythonOperator(
    task_id="model_training",
    python_callable=train_model,
    dag=dag
)

t5 = PythonOperator(
    task_id="model_evaluation",
    python_callable=evaluate_model,
    dag=dag
)

t6 = PythonOperator(
    task_id="model_validation",
    python_callable=validate_model,
    # op_kwargs={'random_base': float(i) / 10},
    # op_args=[],
    dag=dag
)

t1 >> t2 >> t3 >> t4 >> t5 >> t6
