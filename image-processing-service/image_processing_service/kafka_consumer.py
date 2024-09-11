import logging
import base64
import io
from PIL import Image
from kafka import KafkaConsumer, KafkaProducer

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

def process_image(image_bytes):
    '''
    Process the image bytes using the image processor. Turn image in black and white, using pillow.
    Input: 
        image_bytes: bytes
    Output:
        processed_image: bytes
    '''
    # Decode the image bytes
    decoded_bytes = base64.b64decode(image_bytes)
    # Turn the image into black and white using pillow
    image = Image.open(io.BytesIO(decoded_bytes))
    processed_image = image.convert('L')
    # Save the processed image to raw bytes
    buffered = io.BytesIO()
    processed_image.save(buffered, format="PNG")
    processed_image_bytes = buffered.getvalue()
    # Encode the processed image bytes
    processed_image_string = base64.b64encode(processed_image_bytes)
    return processed_image_string



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
