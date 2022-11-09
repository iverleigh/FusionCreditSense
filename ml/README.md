# Fusion CreditSense Machine Learning Service

## About this service
This service is intended to act as a the main Data Science point of entry for the application.
The Edge Service will send requests to this service under instruction from the UI service.
This service will provide a credit score and a credit line suggestion.

## Installation

### Launching api backend as a microservice container
Start by building the container image
~~~
docker build -t mlservice .
~~~

Next, run the container and link it into the fusion-creditsense network
~~~
docker run -d -p 8001:8001 --network=fusion-creditsense --name mlservice mlservice
~~~

## Testing
As a hackathon project for Hack to the Future 2020 hackathon we conducted a large amount of manual testing, however we have not implemented automated testing at this time.

### Folders
- FusionCreditSense.ipynb: Jypiter notebook for Machine Learning work.
- data: Training data. Different versions used: 1, 2, 3_fake76(latest)
- webapp: Code. Python Flask application
    - FusionCreditSenseCLF.pkl: Credit Line suggestion model
    - model_rfr.pkl: Credit line analysis model
    - webapp: flask
        - flask_model_backend.py: Flask model backend for the ML model. Launches a server
        - model_rfr.pkl: The model is a trained random forest regressor
        - test_backend.ipynb: Jupyter notebook to test the flask backend by sending requests to the backend
        - test_data: Data needed to test the backend
