import logging
from image_processing_service.kafka_module.kafka_handler import kafka_consumer, kafka_producer
from image_processing_service.processing_module.dog_detection_image_processor import process_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Started Kafka consumer')
for message in kafka_consumer:
    try:
        request_id = message.key  # Extract the UUID from the message key
        received_string = message.value  # This is received string
        logging.info('Received image from Kafka topic with uuid: %s', request_id.decode('utf-8'))

        # Process the image bytes using the image processor
        image_class_label_bytes = process_image(received_string)
        logging.info('Processed image with image_class_label: %s', image_class_label_bytes.decode('utf-8'))

        # Send the processed image back to Kafka
        kafka_producer.send('image-output-topic', key=request_id, value=image_class_label_bytes)
        logging.info('Sent image_class_label to Kafka topic')
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")
