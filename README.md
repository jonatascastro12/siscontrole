# siscontrole
Enterprise Control System

**SisControle** is a kind of ERP system to help enterprises management.
Now, tt covers people managament, financial and some reports generation.
It is a Django based application.


## Installation

First, you should install python package requirements. 

```
$ pip install -r requirements.txt
```

Then, do Django's basic initialize stuff. Sync your database:

```
$ python manage.py makemigrations
```

```
$ python manage.py migrate
```

```
$ python manage.py syncdb
```

Finally, run the server

```
$ python manage.py runserver
```

