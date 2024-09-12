import logging
from image_processing_service.kafka_module.kafka_handler import kafka_consumer, kafka_producer
from image_processing_service.processing_service import process_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Started Kafka consumer')
for message in kafka_consumer:
    try:
        received_string = message.value  # This is received string
        logging.info('Received image from Kafka topic')
        
        # Process the image bytes using the image processor
        processed_image = process_image(received_string)
        logging.info('Processed image')
        
        # Send the processed image back to Kafka
        kafka_producer.send('image-output-topic', value=processed_image)
        logging.info('Sent processed image to Kafka topic')
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")