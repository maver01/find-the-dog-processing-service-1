# find-the-dog-processing-service-1

Python microservice that handles image processing, for images passed through kafka stream from main java server. Related to the find-the-dog project.

## Description

Main directory tree:

```
├── image_processing_service
│   ├── image_processor.py
│   ├── kafka_consumer.py
```

This repository contains the code related to the microservice that processes the images sent from the server through a kafka stream. It does three main actions:

1. Consume the images from the kafka stream.
2. Apply the custom processing function to each received image.
3. Send the processed image back to a second kafka stream.

The custom function currently simply change turn the picture to black and white.

## Understand the code

- image_processor: The module that handles the custom processing.
- kafka_consumer: The module that handles reading from the first kafka stream and publishing to the second kafka stream.

## Run the code

Assuming python and poetry are installed, run:

```
poetry run python kafka_consumer.py
```
