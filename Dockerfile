# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files for installing dependencies first
COPY pyproject.toml /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Make port 80 available to the world outside this container (80 for HTTP)
EXPOSE 80


# Run app.py when the container launches
CMD ["poetry", "run", "python", "src/processing_service.py"]