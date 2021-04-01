# MLOps
Cloud agnostic tech stack for starting an MLOps platform (Level 1)

"We'll build a pipeline - after we deploy the model."

![Wink](docs/wink.gif)

```Model drift will hit when it's least convenient for you```


__To run__:
Make sure docker is running and you have [Docker Compose](https://docs.docker.com/compose/install/) installed. 

1. Clone the project
    ```bash
    git clone https://github.com/jmeisele/ml-ops.git
    ```
2. Change directories into the repo
    ```bash
    cd ml-ops
    ```
3. Run database migrations and create the first Airflow user account.
    ```bash
    docker-compose up airflow-init
    ```

4. Build our images and launch with docker compose
    ```bash
    docker-compose pull && docker-compose up
    ```
5. Open a browser and log in to [MinIO](http://localhost:9090)

    user: _minioadmin_

    password : _minioadmin_

    Create a bucket called ```mlflow```

    ![MinIO](docs/minio.gif)
6. Open a browser and log in to [Grafana](http://localhost:3000)

    user: _admin_

    password : _admin_

    ![Grafana](docs/grafana_login.gif)
    
    _Both Promethus and InfluxDB data sources have already been provisioned along with an MLOps Demo Dashboard and a Notification Channel._

7. Add the notification channel to some panels 
    ![Panels](docs/alarms_to_panels.gif)
    
8. Start the ```send_data.py``` script which sends a POST request every 0.1 seconds

9. Open a browser and turn on the Airflow DAG used to retrain our ML model

    user: _airflow_

    password : _airflow_

  ![Airflow](docs/airflow_login.gif)

10. Lower the alarm threshold to see the Airflow DAG pipeline get triggered
  
  ![Threshold](docs/lower_threshold.gif)

11. Check [MLFlow](http://localhost:5000) after the Airflow DAG has run to see the model artifacts stored using MinIO as the object storage layer.

12. (Optional) Send a POST request to our model service API endpoint
    ```bash
    curl -v -H "Content-Type: application/json" -X POST -d
    '{
        "median_income_in_block": 8.3252,
        "median_house_age_in_block": 41,
        "average_rooms": 6,
        "average_bedrooms": 1,
        "population_per_block": 322,
        "average_house_occupancy": 2.55,
        "block_latitude": 37.88,
        "block_longitude": -122.23
    }'  
    http://localhost/model/predict
    ```
13. (Optional) If you are so bold, you can also simluate production traffic using locust, __but__ keep in mind you have a lot of services running on your local machine, you would never deploy a production ML API on your local machine to handle production traffic. 

## Level 1 Workflow & Platform Architecture
![MLOps](docs/mlops_level1.drawio.svg)

## Model Serving Architecture
![API worker architecture](docs/ml_api_architecture.drawio.svg)

## Services
- nginx: Load Balancer
- python-model-service1: FastAPI Machine Learning API 1
- python-model-service2: FastAPI Machine Learning API 2
- postgresql: RDBMS
- rabbitmq: Message Queue
- rabbitmq workers: Workers listening to RabbitMQ
- locust: Load testing and simulate production traffic
- prometheus: Metrics scraping
- minio: Object storage
- mlflow: Machine Learning Experiment Management
- influxdb: Time Series Database
- chronograf: Admin & WebUI for InxfluxDB
- grafana: Performance Monitoring
- redis: Cache
- airflow: Workflow Orchestrator
- bridge server: Receives webhook from Grafana and translates to Airflow REST API

## gotchas:

### Postgres:

_Warning: scripts in /docker-entrypoint-initdb.d are only run if you start the container with a data directory that is empty; any pre-existing database will be left untouched on container startup._