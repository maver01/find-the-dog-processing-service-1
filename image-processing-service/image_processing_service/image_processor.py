# image_processor.py

from PIL import Image
import io
import sys

def process_image(image_bytes):
    """
    Process the given image bytes.
    Args:
        image_bytes (bytes): The bytes representing the image.
    Returns:
        bytes: The processed image bytes.
    """
    # Convert bytes to an image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert the image to grayscale (black and white)
    grayscale_image = image.convert("L")
    
    # Save the image to a byte stream
    img_byte_arr = io.BytesIO()
    grayscale_image.save(img_byte_arr, format='JPEG')
    
    return img_byte_arr.getvalue()

if __name__ == "__main__":
    # Read the image bytes from stdin (for Kafka)
    image_bytes = sys.stdin.buffer.read()
    
    # Process the image
    processed_image_bytes = process_image(image_bytes)
    
    # Write the processed image bytes to stdout
    sys.stdout.buffer.write(processed_image_bytes)
