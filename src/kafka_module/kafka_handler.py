import logging
from kafka import KafkaConsumer, KafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka Consumer Configuration
kafka_consumer = KafkaConsumer(
    'image-processing-topic',
    bootstrap_servers=['kafka:9094'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x, # Receive raw bytes
)

# Kafka Producer Configuration
kafka_producer = KafkaProducer(
    bootstrap_servers=['kafka:9094'],
    value_serializer=lambda x: x,  # Send raw bytes
)