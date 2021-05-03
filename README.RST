=============================
Django Rest Framework + Dokku = single server deployment with easy heroku migration
=============================


This is Django Rest Framework adapted to my needs.
It is integrating Redis + RabbitMQ + Postgres + Celery workers.

You can start writing your views, models and tasks, everything will work fine.

Main advantage of this stack is ability to host your application on 10$ server.
But. Once your traffic increases and you need to handle bigger load you can easily
migrate to heroku. Those two are compatible.

On prod statics will be served with Django Whitenoise.

Quickstart
----------

First install pipenv.

.. code-block:: bash

    pip install pipenv

Then run:

.. code-block:: bash

    pipenv shell
    pipenv install

To set up local development we need postgres, redis and rabbitmq.
Install docker if you don't have it.

.. code-block:: bash

    sudo docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
    sudo docker run -d redis
    sudo docker run -d -p 5672:5672 rabbitmq

Run migrations:

.. code-block:: bash

    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate


Then to run a dev server or celery worker:

.. code-block:: bash

    make devserver
    make worker


Dokku server deployment
----------

[You need to install dokku on your server, or pick ready made digital ocean dokku droplet]

Login to your VPS and run those commands (read them first though).


.. code-block:: bash

    # Replace "yourproject" everywhere with your project's name.

    # Create a container for your project.
    sudo dokku apps:create yourproject


    # Install the postgres plugin (you can skip this if you have done it before).
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git

    # Create a database for your project.
    sudo dokku postgres:create yourproject-database

    # Install RabbitMQ plugin.
    sudo dokku plugin:install https://github.com/dokku/dokku-rabbitmq.git rabbitmq

    # Create a RabbitMQ instance for your project.
    sudo dokku rabbitmq:create yourproject-rabbitmq

    # Install the Redis plugin.
    sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis

    # Create a Redis instance for your project.
    sudo dokku redis:create yourproject-redis

    # Link the above instances to your project, this will set up networking
    # and expose environment variables to your project so you can connect.
    sudo dokku postgres:link yourproject-database yourproject
    sudo dokku redis:link yourproject-redis yourproject
    sudo dokku rabbitmq:link yourproject-rabbitmq yourproject

    # I generally like setting this variable so my settings file knows to disable
    # DEBUG and change various other options for running on production.

    # If you don't want the variable to be set globally, just change `--global` to
    # your project's name.
    sudo dokku config:set --no-restart --global NODEBUG=1

    # Add other environment variables to taste.
    sudo dokku config:set --no-restart yourproject SECRET_KEY=somelongkey


You can also add a domain and generate a SSL certificate.
See more here -> https://www.stavros.io/posts/deploy-django-dokku/
