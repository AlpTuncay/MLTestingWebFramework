FROM rabbitmq

WORKDIR /usr/local/bin/
ADD ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
