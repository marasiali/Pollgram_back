import binascii
import os
import pickle

from kafka import KafkaProducer
from json import dumps

from pollgram_back.settings import KAFKA_SERVER

# print(str(KAFKA_SERVER))
vote_producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    # bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: pickle.dumps(v)
)
