# Fusion CreditSense UI Service

## About this service
This service is intended to act as a single point of reference for the User Interface.
This service will send requests to and receive responses from the  Edge Service.

## Installation

### Launching UI Frontend as a microservice container
Start by building the container image
~~~
docker build -t uiservice .
~~~

Next, run the container and link it into the sibos network
~~~
docker run -d -p 4200:4200 --network=fusion-creditsense --name uiservice uiservice
~~~
Just as with the development server approach navigating to `http://localhost:4200/` will provide you with the UI. However be warned that unless you modify the docker container to mount your local filesystem and expose port 49153 on the container then the live reload feature of angular will not work and you will need to rebuild your container and redeploy it for each change.

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).
Note that as this is a hackathon project for Hack to the Future 2020 we haven't implemented any automated testing. However the above command will allow you to run the tests once they exist.

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Note that as this is a hackathon project for Hack to the Future 2020 we haven't implemented any automated testing. However the above command will allow you to run the tests once they exist.

### Folders
- e2e: All of the end to end tests are stored here.
- src: All source code and assets for the application is held in here
-- environments: JSON configuration files for the different environments that we're going to deploy to.
-- assets: Any assets required for the presentation of the user interface are stored here.
--- icons: Specifically we store the icons that we're using in the UI here so they're kept together.
-- app: Source code for all of the application services and features is held in here.