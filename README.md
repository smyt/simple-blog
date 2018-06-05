SMYT blog site
==============

Requirements
------------

* python 3.4
* nodejs with yarn installed
* mysql-server

Settings
--------

1. Create local_settings.py file

    ```
    cp smyt_blog/local_settings.py.sample smyt_blog/local_settings.py
    ```

    edit it.

2. Install python requirements

    ```
    pip install -r requirements.txt
    ```

3. Install nodejs requirements

    ```
    yarn install
    ```

4. Create and run migrations

    ```
    python manage.py makemigrations && python manage.py migrate
    ```

5. Create superuser for admin access

    ```
    python manage createsuperuser
    ```

Collect static
--------------
For static collection run next commands

```
yarn build_styles
python manage.py collectstatic
```


Application deployment
-----------------

Create fabfile.py by copying sample

```
cp fabfile.py.sample fabfile.py
```

edit CONFIG variable

```
CONFIG = {
    'dev': {
        'host': 'user@server',
        'activate': 'source /home/user/virtualenv/blog/bin/activate',
        'code_folder': '/home/user/blog'
    }
}
```

Run

```
fab dev deploy
```


Deployment with gunicorn + upstart + nginx
----------------------------------------------------------------------

Make sure that media folder has all required access rights 

File nginx.conf

```
server {
    listen 80;
    server_name blog.test.smytsoft.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/user/blog;
    }

    location /media/ {
        root /home/user/blog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/blog/blog.sock;
    }
}
```

file gunicorn.conf

```
import multiprocessing

bind = 'unix:/home/user/blog/blog.sock'
pidfile = '/home/user/blog/blog.pid'
user = 'www-data'
group = 'www-data'
workers = multiprocessing.cpu_count() * 2 + 1

errorlog = './logs/error.log'
accesslog = './logs/access.log'
```

file upstart.conf

```
description "smyt-blog-site gunicorn process"

start on runlevel [2345]
stop on runlevel [!2345]

respawn

chdir /home/user/blog
exec /home/user/virtualenv/blog/bin/gunicorn --config configs/gunicorn_config.py smyt_blog.wsgi:application
```
