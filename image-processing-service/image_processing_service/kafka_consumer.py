# kafka_consumer.py
"""
This script is responsible for consuming images from a Kafka topic, processing them using the image_processor module, and producing the processed images to another Kafka topic.

Attributes:
    consumer (KafkaConsumer): The Kafka consumer instance used to consume images from the 'image-input-topic'.
    producer (KafkaProducer): The Kafka producer instance used to produce processed images to the 'image-output-topic'.
"""


from kafka import KafkaConsumer, KafkaProducer
from image_processing_service import image_processor

consumer = KafkaConsumer(
    'image-input-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x
    )

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: x)

for message in consumer:
    image_bytes = message.value
    processed_image_bytes = image_processor.process_image(image_bytes)
    producer.send('image-output-topic', value=processed_image_bytes)
