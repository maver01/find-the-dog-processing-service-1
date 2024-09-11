import base64
import io
from PIL import Image

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
