# SMS API

This example is written with Django 1.8.1.

## Building
### Install PIP
PIP is needed for python dependency management. Install pip and upgrade to latest version.
```sh
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```

### Virtual Environment
It is best to use the python `virtualenv` tool to build locally:

```sh
$ sudo pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```
### Install Requirements
Few linux packages or libraries are required for python dependencies to get installed.  
sudo apt-get install libpq-dev .   
sudo apt-get install python-dev .  
sudo apt-get install libffi-dev .   
sudo apt-get install python-cffi .   
```sh
$ pip install -r requirements.txt
```
### DB Setup
Follow instructions from the link to install Postgres server locally.
https://help.ubuntu.com/community/PostgreSQL

create a database on the local db server .   
import dump to the created db - psql dbname < dumpfile .   
dump is in code base smsapi/smsapi.psql . 

Add following environment variables to virtual environment's activate file .   
RDS_DB_NAME="smsapi" .  
RDS_USERNAME="postgres" .   
RDS_PASSWORD="postgres" .   
RDS_HOSTNAME="localhost" .   
RDS_PORT="5432" .   

### Run server
Run all django commands from virtual environment only  
```sh
$ python manage.py runserver
```

### Run tests
```sh
$ python manage.py test api.tests
```

