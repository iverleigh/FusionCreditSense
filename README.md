# Fusion CreditSense
Fusion CreditSense - Giving credit where credit is due.<br> 
Winner of the Hack to the Future Hackathon 2020 for Best Social Impact. <br>
Team members: IV Yoo (ML), Philip Crisp (Software Dev), Alan Prowse-McLean (Software Dev), and Chloe Luo (UI/UX).<br>
https://devpost.com/software/fusion-creditsense


## Folder structure
- edgeservice: Edge service module to bring all the components together module [README](./edgeservice/README.md)
- ml: Machine Learning module [README](./ml/README.md)
- uiservice: User Interface module [README](./uiservice/README.md)

## Installation

### Prerequisites
* Docker
Note: These instructions were written for a Linux VM. If you're building on a Windows host then you may need to alter the commands somewhat.

### Building the network
Start with a Linux VM instance with docker installed
~~~
docker network create -d bridge fusion-creditsense
docker build -t edgeservice edgeservice/
docker build -t uiservice uiservice/
docker build -t mlservice ml/
~~~

### Start the containers
Note: The port numbers are very important
Start by switching back to the Linux VM.
We recommend starting with the uiservice image as the runtime compilation for the packages used there takes some time to finish and doing that one first will reduce wait time.
~~~
docker run -d -p 4200:4200 --network=fusion-creditsense --name uiservice uiservice
docker run -d -p 8000:8000 --network=fusion-creditsense --name edgeservice edgeservice
docker run -d -p 8001:8001 --network=fusion-creditsense --name mlservice mlservice
~~~

### Final set up
Now that you've got the contianers running we need to make sure that the DB is set up properly for the edge service.
Start by running the Alpine linux ASH command to access the terminal
~~~
docker exec -ti edgeservice /bin/ash
~~~
Finally run the django migrations
~~~
python manage.py migrate
~~~
Note: We're using an sqllite database here, however for production environments we would recommend using a dedicated database .

## Using the Application
Visit IPADDRESS / HOSTNAME on port 4200 to load the UI.
You will need a test company on the Fusion OpenBanking system as well as a username and password for performing HTTP Basic Auth during requests.

## Working with the containers
You can now use any commands supported by docker in order to work with these containers.
We recommend docker logs -f CONTAINER_NAME if you're curious about what's going on under the hood as there is some useful debugging going on there.

## More information information
More  information about each service is available inside each services individual README.md file (linked above)
