=============================
Django Rest Framework + Dokku = single server deployment with easy heroku migration
=============================

.. image:: https://img.shields.io/pypi/v/django-payments-przelewy24
    :target: https://pypi.org/project/django-payments-przelewy24/

.. image:: https://circleci.com/gh/ar4s/django-payments-przelewy24.svg?style=shield
    :target: https://circleci.com/gh/ar4s/django-payments-przelewy24


This is Django Rest Framework adapted to my needs.
It is integrating Redis + MySQL + Celery workers
There are example views and tasks added.


Quickstart
----------

Install pipenv:

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

test
