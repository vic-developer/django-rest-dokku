
help:
	@echo 'Makefile for local development                                            '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make devserver [PORT=8000]      serve and hot reload                   '
	@echo '   make worker                     fire up a celery worker with rabbitmq  '
	@echo '                                                                          '
	@echo '                                                                          '

devserver:
	pipenv run python manage.py runserver

worker:
	pipenv run celery -A api worker --loglevel=INFO


.PHONY: html help clean regenerate serve serve-global devserver publish github