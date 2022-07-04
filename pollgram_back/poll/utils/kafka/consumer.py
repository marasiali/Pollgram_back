import os
import pickle

from kafka import KafkaConsumer

from poll.models import Vote

vote_consumer = KafkaConsumer(
    'votes',
    bootstrap_servers=[os.environ.get('KAFKA_SERVER')],
    # bootstrap_servers=['localhost : 9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='group',
    value_deserializer=lambda v: pickle.loads(v),
    max_poll_records=1000
)

for message in vote_consumer:
    message = message.value
    print('message' + str(message))
    created_vote = Vote.objects.create(user=message.user)
    created_vote.selected.set(message.choices)
