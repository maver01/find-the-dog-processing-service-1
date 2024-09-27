import logging
from image_processing_service.kafka_module.kafka_handler import kafka_consumer, kafka_producer
from image_processing_service.processing_module.dog_detection_image_processor import process_image

# Import the Prometheus client libraries
from prometheus_client import start_http_server, Counter, Histogram, Gauge

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a counter for processed images
IMAGE_PROCESSED_COUNTER = Counter('images_processed', 'Total number of images processed')
# Create a histogram to track processing time, in seconds
IMAGE_PROCESSING_TIME = Histogram('image_processing_duration_seconds', 'Histogram for image processing duration')
# Create a counter for image processing errors
ERROR_COUNTER = Counter('image_processing_errors', 'Total number of image processing errors')
# Create a gauge to track the current number of images being processed
PROCESSING_GAUGE = Gauge('images_processing_current', 'Current number of images being processed')

# Start the Prometheus metrics server
start_http_server(8000)

logging.info('Started Kafka consumer')
for message in kafka_consumer:
    try:
        PROCESSING_GAUGE.set(1)  # Set to 1 when processing starts
        request_id = message.key  # Extract the UUID from the message key
        received_string = message.value  # This is received string
        logging.info('Received image from Kafka topic with uuid: %s', request_id.decode('utf-8'))

        # Measure processing time, unit: seconds
        with IMAGE_PROCESSING_TIME.time():
            # Process the image bytes using the image processor
            image_class_label_bytes = process_image(received_string)
        
        IMAGE_PROCESSED_COUNTER.inc()  # Increment the processed images counter     
        logging.info('Processed image with image_class_label: %s', image_class_label_bytes.decode('utf-8'))

        # Send the processed image back to Kafka
        kafka_producer.send('image-output-topic', key=request_id, value=image_class_label_bytes)
        logging.info('Sent image_class_label to Kafka topic')

        PROCESSING_GAUGE.set(0)  # Reset to 0 after processing
    
    except Exception as e:
        ERROR_COUNTER.inc()  # Increment the error counter
        logging.error(f"Error processing message: {e}")
