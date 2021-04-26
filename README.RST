=============================
Django Rest Framework + Dokku = single server deployment with easy heroku migration
=============================


This is Django Rest Framework adapted to my needs.
It is integrating Redis + RabbitMQ + MySQL + Celery workers
There are example views and tasks added.


Quickstart
----------

First install pipenv.

Then run:

.. code-block:: bash

    pipenv shell
    pipenv install

To set up local development we need redis and rabbitmq.
Install docker if you don't have it.

.. code-block:: bash

    docker start redis
    docker run -d -p 5672:5672 rabbitmq

Then to run a dev server or celery worker:

.. code-block:: bash

    make devserver
    make worker


Dokku server deployment
----------

Login to your VPS and run those commands. (read them first though)
stolen from: https://www.stavros.io/posts/deploy-django-dokku/

.. code-block:: bash
    
    # Replace "yourproject" everywhere with your project's name.

    # Create a container for your project.
    sudo dokku apps:create yourproject


    # Install the postgres plugin (you can skip this if you have done it before).
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git

    # Create a database for your project.
    sudo dokku postgres:create yourproject-database


    # Install the Redis plugin.
    sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis

    # Create a Redis instance for your project.
    sudo dokku redis:create yourproject-redis

    # Link the above instances to your project, this will set up networking
    # and expose environment variables to your project so you can connect.
    sudo dokku postgres:link yourproject-database yourproject
    sudo dokku redis:link yourproject-redis yourproject

    # I generally like setting this variable so my settings file knows to disable
    # DEBUG and change various other options for running on production.

    # If you don't want the variable to be set globally, just change `--global` to
    # your project's name.
    sudo dokku config:set --no-restart --global NODEBUG=1

    # Add other environment variables to taste.
    sudo dokku config:set --no-restart yourproject SECRET_KEY=somelongkey