# base image
FROM python:3.7.2-alpine

# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set working directory
WORKDIR /usr/src/ml-framework

# add and install requirements
COPY ./requirements.txt /usr/src/ml-framework/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/ml-framework/entrypoint.sh
RUN chmod +x /usr/src/ml-framework/entrypoint.sh

# add app
COPY . /usr/src/ml-framework

# run server
CMD ["sh", "/usr/src/ml-framework/entrypoint.sh"]
