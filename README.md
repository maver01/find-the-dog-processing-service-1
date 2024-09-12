# find-the-dog-processing-service-1

Python microservice that handles image processing, for images passed through kafka stream from main java server. Related to the find-the-dog project.

## Description

Main directory tree:

```
├── image_processing_service
│   ├── kafka_module
│   │   └── kafka_handler.py
│   ├── processing_module
│   │   └── image_processor.py
│   ├── processing_service.py

```

This repository contains the code related to the microservice that processes the images sent from the server through a kafka stream. It does three main actions:

1. Consume the images from the kafka stream.
2. Apply the custom processing function to each received image.
3. Send the processed image back to a second kafka stream.

The custom function currently simply change turn the picture to black and white.

## Understand the code

- kafka_module: The module that handles reading from the first kafka stream and publishing to the second kafka stream, and it's configuration.
- processing_module: The module that handles the processing of the image.
- processing_service.py: The module to run, that reads messages, processes them, and write them to the second kafka topic.

## Run the code

Assuming python and poetry are installed, run:

```
poetry run python processing_service.py
```
