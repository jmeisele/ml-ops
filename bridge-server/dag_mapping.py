"""
Author: Jason Eisele
Date: February 26, 2021
Scope: Map of DAGs to push POST requests to Airflow from Grafana 
        based on alert rules
"""

dag_config_map = {
    "Model Error Monitoring alert": "python_example_ml_retrain"
}