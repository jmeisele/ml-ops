from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas_profiling as pp
import pandas as pd
import mlflow
from mlflow.sklearn import save_model
from mlflow import log_metric, log_param, log_artifacts

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
    data = datasets.fetch_california_housing(as_frame=True).frame
    feature_columns = {
        "MedInc": "median_income_in_block",
        "HouseAge": "median_house_age_in_block",
        "AveRooms": "average_rooms",
        "AveBedrms": "average_bedrooms",
        "Population": "population_per_block",
        "AveOccup": "average_house_occupancy",
        "Latitude": "block_latitude",
        "Longitude": "block_longitude",
        "MedHouseVal": "median_house_value",
    }
    dataset = data.rename(columns=feature_columns)
    dataset.to_csv("dataset.csv")
    return dataset


def validate_data():
    valid_data = "Yep, looks good"
    return valid_data


def prep_data():
    df = pd.read_csv("dataset.csv")
    features = [
        "median_income_in_block",
        "median_house_age_in_block",
        "average_rooms",
        "average_bedrooms",
        "population_per_block",
        "average_house_occupancy",
        "block_latitude",
        "block_longitude",
    ]
    X = df[features]
    y = df["median_house_value"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    model = sklearn.linear_model.LinearRegression()
    "Log Hyperparameters, Metrics & Model to MLFlow"
    mlflow.sklearn.autolog()
    mlflow.set_tracking_uri("https://mlflow.ds.us-east-1.shipt.com/")
    # Give your experiment a name
    mlflow.set_experiment(experiment_name="ml-ops-demo")
    with mlflow.start_run() as run:
        model.fit(X_train, y_train)
        mlflow.log_artifact("Raw_Data_Profile.html")
    return model


def evaluate_model(model):
    model_evaluated = "Looks great so far, let's check new data"
    model.score(X_train, y_train)
    return model_evaluated


def validate_model(model, X_test, y_test):
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
