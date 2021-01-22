##Hosted Application Url
https://casting-agency-22.herokuapp.com/

##Casting Agency
The project is to simulate a casting agency. This includes having actors and movies and assigning actors to movies

##Database
There are many-to-many relationship between Movie and Actor.

##Motivation for project
This is the capstone project of Udacity fullstack nanodegree program, which demonstrate the skillset of using Flask, SQLAlchemy, Auth0, gunicorn 
and heroku to develop and deploy a RESTful API.

##Getting Started
#Installing Dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

###Database Setup
To test endpoints, with Postgres running, restore a database using the castingagency.sql file provided. From the file directory in terminal run:
```
psql castingagency < castingagency.sql
```

##Running the server
From within the file directory first ensure you are working using your created virtual environment.

To run the server, execute:
```
python3 app.py
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

#####Tasks
#####Setup Auth0
1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `add:actors`
    - `add:movies`
    - `delete:actors`
    - `delete:movies`
    - `edit:actors`
    - `edit:movies`
    - `view:actors`
    - `view:movies`
6. Create new roles for:
 -Casting Assistant
   -Can view actors and movies`
 -Casting Director
   -All permissions a Casting Assistant has and ...
   -Add or delete an actor from the database
   -Modify actors or movies
 -Executive Producer
   -All permissions a Casting Director has and ...
   -Add or delete a movie from the database
7. Test your endpoints with Postman.
   -Register 3 users - assign the Casting Assistant role to one and Casting Director role to another, and Executive Producer to the other.
   -Sign into each account and make note of the JWT.
   -Test each endpoint and correct any errors.