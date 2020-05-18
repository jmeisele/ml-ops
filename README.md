# MicroModel
Handling MLOps as a microservice

__To install__:

1. Clone the project
    ```bash
    git clone https://github.com/jmeisele/MicroModel.git
    ```
2. Change directories into the repo
    ```bash
    cd MicroModel
    ```
3. Run docker compose
    ```bash
    docker-compose up
    ```
4. Open up a new terminal window and send a POST request to our model service API endpoint
    ```bash
    curl -d "name=mercedes&price=200" -X POST http://localhost:8080/predict
    ```
<!-- 5. Next in the terminal window, buy the item you just created
    ```bash
    curl -d "name=mercedes" -X POST http://localhost:3002/buy
    ``` -->
6. This sends a message to the queue being managed by our RabbitMQ broker for the Python factory service to build

_ProTip_ Check the status/health of all running containers using Portainer

[Portainer](http://localhost:9000)

# TODOs
- [ ] Construct docker compose file to get all services up and running

If you found this repo helpful, a [small donation](https://www.buymeacoffee.com/VlduzAG) would be greatly appreciated. 
All proceeds go towards coffee, and all coffee goes towards more code.