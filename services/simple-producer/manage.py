from rabbitmq_producer import Producer
import time
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    producer = Producer()

    num_msg = 1000

    for i in range(num_msg):
        msg = "A Message no:%d from Producer to Consumer" % i
        msg = str.encode(msg)
        producer.produce_msg(msg)

        logging.info(f"{msg} should have been sent.")
        time.sleep(5)

