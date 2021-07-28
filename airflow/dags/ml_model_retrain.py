from datetime import timedelta
import pickle

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas_profiling as pp
import pandas as pd
import mlflow
import numpy as np
from mlflow import log_metric, log_param, log_artifacts
from boxkite.monitoring.service import ModelMonitoringService
# from mlflow.sklearn import save_model


default_args = {
    "owner": "Jason",
    "email": "mlops@community.com",
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
    dataset.to_csv("raw_data.csv")
    return "Pull data done!"


def validate_data():
    # Slot in great expectations here?
    dataset = pd.read_csv("raw_data.csv")
    profile_report = pp.ProfileReport(dataset)
    profile_report.to_file("raw_data_profile.html")
    return "Raw Data Profiled!"


def prep_data():
    df = pd.read_csv("raw_data.csv")
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
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    with open("X.pkl", "wb") as file:
        pickle.dump(X, file)
    with open("X_train.pkl", "wb") as file:
        pickle.dump(X_train, file)
    with open("X_test.pkl", "wb") as file:
        pickle.dump(X_test, file)
    with open("y_train.pkl", "wb") as file:
        pickle.dump(y_train, file)
    with open("y_test.pkl", "wb") as file:
        pickle.dump(y_test, file)
    return "Data prepped, ready for training"


def train_model():
    with open("X_train.pkl", "rb") as f:
        X_train = pickle.load(f)
    with open("y_train.pkl", "rb") as f:
        y_train = pickle.load(f)
    model = LinearRegression()
    "Log Hyperparameters, Metrics & Model to MLFlow"
    mlflow.sklearn.autolog()
    mlflow.set_tracking_uri("http://mlflow:5000")
    # Give your experiment a name
    mlflow.set_experiment(experiment_name="ml-ops-demo")
    mlflow.start_run()
    # with mlflow.start_run() as run:
    model.fit(X_train, y_train)
    mlflow.log_artifact("raw_data_profile.html")

    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)
    return "Model trained and logged!"


def evaluate_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("X_train.pkl", "rb") as f:
        X_train = pickle.load(f)
    with open("y_train.pkl", "rb") as f:
        y_train = pickle.load(f)
    print(model.score(X_train, y_train))
    return "Looks great so far, let's check new data"


def validate_model():
    with open("X.pkl", "rb") as file:
        X = pickle.load(file)

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("y_test.pkl", "rb") as f:
        y_test = pickle.load(f)

    with open("X_test.pkl", "rb") as f:
        X_test = pickle.load(f)

    # Model Evaluation
    y_pred_test = model.predict(X_test)
    holdout_mse = mean_squared_error(y_test, y_pred_test)
    holdout_rmse = np.sqrt(holdout_mse)
    holdout_mae = mean_absolute_error(y_test, y_pred_test)
    holdout_med = (y_test - y_pred_test).median()
    holdout_r2 = r2_score(y_test, y_pred_test)

    # Log our testing metrics, autolog takes care of the training metrics
    mlflow.log_metric("testing_rmse", holdout_rmse)
    mlflow.log_metric("testing_mae", holdout_mae)
    mlflow.log_metric("testing_mse", holdout_mse)
    mlflow.log_metric("testing_median_error", holdout_med)
    mlflow.log_metric("testing_r2_score", holdout_r2)

    # Log our training and inference distributions
    features = X.iteritems()
    inference = list(y_pred_test)

    ModelMonitoringService.export_text(
        features=features,
        inference=inference,
        path="./histogram.prom",
    )
    mlflow.log_artifact("./histogram.prom")
    mlflow.end_run()
    return "Even performs great on new data"


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
