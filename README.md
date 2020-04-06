# Monitoring API

## Overview
Web Database Project (Loyola COMP-453)
http://cnaiman.com/COMP353-453/Project/ProjectOverview.html

Git Repository
https://gitlab.com/loyola-monitor

Good step-by-step tutorial:
https://github.com/paurakhsharma/flask-rest-api-blog-series/blob/master/Part%20-%200/Part-0%20Hello%20Flask%20Rest%20API.md

## Start developing
source venv/bin/activate && pip install -r requirements.txt

## Dependencies
Flask
    https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request
    
Flask-SQLAlchemy
    pip install mysqlclient 
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/
    SQLAlchemy Examples
    https://www.bradcypert.com/writing-a-restful-api-in-flask-sqlalchemy/

Flask-Bcrypt
    pip install flask-bcrypt
    https://flask-bcrypt.readthedocs.io/
    
Flask-JWT
    pip install flask-jwt-extended
    https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    
marshmallow - simplified object serialization¶
    pip install marshmallow
    https://marshmallow.readthedocs.io/en/stable/

## First setup
Create an environment¶
```
$ python3 -m venv venv
```

Activate / Deactivate
```
$ source venv/bin/activate
$ deactive
```

Create dependency file
```
$  pip freeze > requirements.txt
```
