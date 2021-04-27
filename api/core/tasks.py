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
  logger.info(data)
  try:
    qs = User.objects.first()
    if qs:
      logger.info('Got the user and DB connection from celery works!')
    else:
      logger.error('No user, creating wiktor')
      u = User.objects.create(email='wiktor@lol.com')
      u.save()

  except Exception as exc: # in real life it should be a specific exception
    # overrides the default delay to retry after 1 minute
    logger.error('something is wrong')
    logger.error(exc)
    raise self.retry(exc=exc, countdown=60)

