FROM python:3.8.5
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# Install some necessary dependencies.
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

# Install the requirements. This is done early so the requirements
# don't need to be reinstalled every time something unrelated changes,
# which would otherwise happen due to the way Docker does image
# caching.
RUN pip install pipenv

# Copy the code and collect static media.
# You can use whitenoise to serve them, or CloudFront to proxy them.
WORKDIR /code
COPY . /code/

ADD Pipfile.lock /code/
RUN pipenv install --system --deploy --ignore-pipfile

# create and change user
RUN useradd -ms /bin/bash app-runner
RUN chown -R app-runner:app-runner /code

USER app-runner


# Add the Dokku-specific files to their locations.
ADD dokku/CHECKS /app/
ADD dokku/* /code/
