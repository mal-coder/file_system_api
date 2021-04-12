--------------------
# File system  API
Simple REST API allowing access to information about files and folders in the file system. 
## Prerequisites
(if you do not wish to install anything use the attached *docker-compose* file.):
* Python 3.9
* Pipenv
* Postgres DB

optionally: 
* Docker

## Installing File system API

To install File system API, follow these steps:
* Clone the repository and create a virtual environment with pipenv to install all the needed libraries
```
$ pipenv install
```
Create the following environmental variables:
```
ROOT_PATH=./file-system-data/ - root path for storing files
DB_URI=postgresql://localhost/postgres
SALT=zz87 - access token salt
ROOT_PWD=4c183e2729c2effc23623sd224 - root password to create user access tokens
DEBUG=False
```

## Using File system API

To use File system API simply start it with:
```
python run.py 
```
Or use the provided `docker-compose.yml`. 

To see the endpoints description go to:
```
http://localhost:5050/swagger/
```

All endpoints are authenticated with a `Bearer` token. For `root` endpoint use the `ROOT_PWD` token.
For the rest of the endpoints use tokens generated using `root/create_token/` endpoint. Each token is tied 
to a separate/user unique dictionary within the file system. 

### Testing File system API

To test File system API run:
```
docker-compose run filesystem-api sh -c "pytest tests"
```
