# Fusion CreditSense Edge Service

## About this service
This service is intended to act as a middle-man between the UI, our custom back-end services and third party systems.
This service has been written in Python with Django and the Django Rest Framework to provide API services and sessions across a number of different services.

## Installation

### Launching backend api in a virtual machine
Start by defining a virtual environment
~~~
python3 -m venv finclude
source finclude/bin/activate
~~~
Next you need to install the required dependencies
~~~
pip install -r requirements.txt
~~~
Now you're ready to run the server
~~~
python manage.py runserver 0.0.0.0:8000
~~~

### Launching api backend as a microservice container
Start by building the container image
~~~
docker build -t edgeservice .
~~~

Next, run the container and link it into the sibos network
~~~
docker run -d -p 8000:8000 --network=fusion-creaditsense --name edgeservice edgeservice
~~~

## Testing
As a hackathon project for Hack to the Future 2020 hackathon we conducted a large amount of manual testing, however we have not implemented automated testing at this time.
To run any automated tests that are developed in the future you can run:
~~~
python manage.py test
~~~

### Folders
- api: The API views and associated code required for the screens and making the various API calls to other services
- utils: Useful utilities leveraged for the project, this includes a script to generate a potentially unlimited amount of OpenBanking sample data for training models.
- edgeservice: The configuration and settings for the service to run via Django and Python.