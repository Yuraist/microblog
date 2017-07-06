# Microblog
**_Microblog_** is a web application written using the Flask framework.
An idea is the website like Twitter. You can register and login, write posts, follow and read other users. 
You can also edit your profile adding description and avatar. 

## How to use
To start with **_Microblog_** you should install all requirements which stored in _requirements.txt_ file.

```pip install requirements.txt```

When you install all the requirements you should initialize the database.
**_Microblog_** uses PostgreSQL database for storing of data.

Don't forget to run the PostgreSQL on your machine and create the database.
Also you should change `SQLALCHEMY_DATABASE_URI` in the _config.py_ file.

```
$ python run.py db init
```

After initialization migrate and upgrade the database to create tables from model.
When you update your model you also need to `migrate` and `upgrade` your db.

``` 
$ python run.py db migrate
$ python run.py db upgrade 
```

## Description
The project is created for educational purposes so it can contain some errors and imperfections. 
But you can play with it and use for your own projects. Some of the code may be very useful for you.
