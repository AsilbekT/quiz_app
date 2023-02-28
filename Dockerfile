# Pull base image
FROM python:3.10
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code

ADD . /code

# install dependencies  
COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

# Copy project
COPY . /code/