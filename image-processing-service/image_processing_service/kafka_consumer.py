import logging
from kafka import KafkaConsumer, KafkaProducer
from image_processing_service.image_processor import process_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'image-processing-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x, # Receive raw bytes
)

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: x,  # Send raw bytes
)

logging.info('Started Kafka consumer')
for message in consumer:
    try:
        received_string = message.value  # This is received string
        logging.info('Received image from Kafka topic')
        
        # Process the image bytes using the image processor
        processed_image = process_image(received_string)
        logging.info('Processed image')
        
        # Send the processed image back to Kafka
        producer.send('image-output-topic', value=processed_image)
        logging.info('Sent processed image to Kafka topic')
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")
