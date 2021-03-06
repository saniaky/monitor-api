# Monitoring API

## Overview
Web Database Project (Loyola COMP-453)
- [Project requirements](http://cnaiman.com/COMP353-453/Project/ProjectOverview.html)
- [Git Repository](https://gitlab.com/loyola-monitor)
- [Good step-by-step tutorial](https://github.com/paurakhsharma/flask-rest-api-blog-series/blob/master/Part%20-%200/Part-0%20Hello%20Flask%20Rest%20API.md)

## Features
- User registration
- User login
- Update user profile
- Create app for monitoring
- Update app for monitoring

- Add app maintenance info
- Add app incident info


## Dependencies
- [Flask - web framework](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request)  
- [SQLAlchemy - Object Relational Mapper](https://docs.sqlalchemy.org/en/13/orm/tutorial.html)
    - [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/13/orm/relationships.html)
    - [Query Update API](https://docs.sqlalchemy.org/en/13/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.update)
    - [Database Model Representation](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers)
- [Flask-SQLAlchemy - SQLAlchemy wrapper for Flask](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)  
    - [Examples](https://www.bradcypert.com/writing-a-restful-api-in-flask-sqlalchemy/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)  
- [Flask-JWT - manage JWT tokens](https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/)  
- [marshmallow - serialization and validation](https://marshmallow.readthedocs.io/en/stable/)  
    - [Existing validators](https://marshmallow.readthedocs.io/en/stable/_modules/marshmallow/validate.html)

## First setup

### Quick start
```
source venv/bin/activate && pip install -r requirements.txt
```

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
