# testPythonNeolegal
Here is all the instructions to test this Python FastAPI App
## Docker and Docker compose
To run the project you need docker then docker compose

Here is the documentation for Linux (but you can find different OS installation)
Docker:
[Install Docker Engine on Ubuntu | Docker Docs](https://docs.docker.com/engine/install/ubuntu/)

Docker compose:
[Install the Compose plugin | Docker Docs](https://docs.docker.com/compose/install/linux/)

if  ``docker run hello-world `` render ``Hello from Docker!``

 #### and
``docker compose version`` gives you ``Docker Compose version vN.N.N``

### Then we are good to go
## Build the Docker image and run !

In order to launch our app we need to build the docker image. In a better way it will be nice to have a docker registry to avoid builds problem and a fastest setup for the test.

run this command in order to build our Docker image and launch our App and Mysql via docker-compose:

``docker compose up -d``
 This will take ~ 5 mn you may want to launch the other project buid or get a Cofee ☕
##  Health check and tests !

Now server is available, you can check it via the doc on FastAPI auto-generated docs

``http://localhost:8000/docs``

Then you can import Postman collection and environment for tests via the folder
``/postman_tests``

## Shutdown and uninstall
To shutdown the Test App run the docker compose down with extra for DB volumes

 ``docker compose down -v``

and now you can run the docker system prune to remove unused images and containers

 ``docker system prune``
