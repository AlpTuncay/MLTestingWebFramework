# base image
FROM postgres:11.2-alpine


# run init.sql on init
ADD init.sql /docker-entrypoint-initdb.d
