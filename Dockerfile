# Use an official Python base image
FROM python:3.10-slim-buster
# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install spaCy language model
RUN python -m spacy download en_core_web_sm


# Expose the port FastAPI will run on
EXPOSE 7860

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
