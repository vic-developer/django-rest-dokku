import os

import redis
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User


logger = get_task_logger(__name__)

redis_instance = redis.from_url(os.environ.get("REDIS_URL", ""), db=0)


@task(name="find_first_user", bind=True, default_retry_delay=30)
def find_first_user(self, data):
  logger.info("looking for user")
  logger.info("got some data!", data)

  try:
    qs = User.objects.first()
    if len(qs) == 0:
      logger.error('couldnt find user')
    elif len(qs) == 1:
      logger.info('found the user yaay')
    else:
      logger.error('this should never happend, django bad')

  except Exception as exc: # in real life it should be a specific exception
    # overrides the default delay to retry after 1 minute
    raise self.retry(exc=exc, countdown=60)

