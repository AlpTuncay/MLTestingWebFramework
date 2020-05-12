FROM rabbitmq:3.7

WORKDIR /usr/local/bin/
ADD ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
