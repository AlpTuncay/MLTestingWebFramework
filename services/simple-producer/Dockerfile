# base image
FROM python:3.7.2-alpine

# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set working directory
WORKDIR /usr/src/ml-framework/producer

# add and install requirements
COPY ./requirements.txt /usr/src/ml-framework/producer/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/ml-framework/producer/entrypoint.sh
RUN chmod +x /usr/src/ml-framework/producer/entrypoint.sh

# add app
COPY . /usr/src/ml-framework/producer

# run server
ENTRYPOINT ["sh", "/usr/src/ml-framework/producer/entrypoint.sh"]