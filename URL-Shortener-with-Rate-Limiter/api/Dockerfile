# Start from an existing python image.
FROM python:3.13-alpine
# Inside the container, change directory to /app. If it does not exist, create it. /app is the project root inside the container
WORKDIR /app 
# Optimise Docker's use of layers. Code is more likely to change then requirements.txt
COPY requirements.txt .
# Install the requirements without cache to save image size
# RUN is used for build-time commands
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy the remaining files into the image
COPY . . 
# The command to start up the application (In this case the FastAPI application)
# Spin up a manual uvicorn server. Host 0.0.0.0 means listen to all network interfaces. 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

