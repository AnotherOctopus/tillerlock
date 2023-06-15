FROM python:3.7-slim as base

# send python logs to the console
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# set /app path as the default directory inside the container
WORKDIR /app

# copy the requirements into the container
COPY ./requirements.txt /app/requirements.txt

# required for pip install ps-protos
RUN apt-get update  \
    && apt-get install -y g++

# install all requirements
RUN pip install -r requirements.txt



########################################
FROM base as production

# copy this project into the container
COPY . /app

# start the flask app
CMD ["flask", "run", "--host", "0.0.0.0"]



########################################
FROM production as development

# add awscli for development convenience
RUN pip install awscli

# add flake8 for linting for development convenience
RUN pip install flake8

# add git for development convenience
RUN apt-get update
RUN apt-get -y install git
