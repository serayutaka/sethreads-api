# Use an official Python runtime as a parent image
# Use a more specific base image that supports multiple architectures
FROM --platform=$TARGETPLATFORM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /code

# Set build arguments for architecture
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

# Copy and install requirements first (for better caching)
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application files
COPY ./config /code/config
COPY ./static /code/static
COPY ./static/templates /code/static/templates
COPY ./static/uploads /code/static/uploads
COPY ./src /code/src

# Set the command to run the application
CMD ["fastapi", "run", "src/app.py"]