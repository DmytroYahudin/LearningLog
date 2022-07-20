# Learning Log
This is the simple Learning Log pet project created base on Django framework.
The purpose of it is just to log your new knowlages or achievments. 

## Installation
In order to pull the repository and run the web application you may follow the next steps:

Create project directory
Linux/Windows:
```bash
mkdir <your_project_directory>
```
Go to created directory:
```bash
cd <your_project_directory/>
```
Clone repository from GitHub via command:
```github
git clone https://github.com/DmytroYahudin/LearningLog.git
```
In order to build docker container you need to installed [Docker](https://docs.docker.com/compose/gettingstarted/) in your system.
Make sure that Docker is installed on your PC, build the image and run the container:\
Linux:
```bash
sudo docker build --tag my_log .
```
Windows:
```bash
docker build --tag my_log .
```

After image is built run the container using the following command:
```bash
docker run --name log_app -d -p 8000:8000 my_log 
```

Make sure the container is up and running. You can use Docker Desktop application or enter docker ps in terminal.\
You can create an admin user:
```bash
docker exec -w /app_log/my_log -it log_app python manage.py createsuperuser
```

Now you can log in into the application.

## Tests
There are 50 test cases already written in the application. In order to run the unit tests use the following command:
```bash
docker exec -w /app_log/my_log -it log_app python manage.py test
```

## Usage

You can access to the web application by following the link [http://localhost:8000/](http://localhost:8000/)
Also you can access as an admin to the django admin site by following the link [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## References
[Learning Log at GitHub.com](https://github.com/DmytroYahudin/LearningLog/)
