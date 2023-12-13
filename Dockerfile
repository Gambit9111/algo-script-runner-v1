# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

ADD ./bot /app/bot
ADD .env /app/.env
ADD requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME FLASK_SECRET_KEY
ENV NAME ADMIN_USERNAME
ENV NAME ADMIN_USERNAME
ENV NAME BYBIT_API_KEY
ENV NAME BYBIT_API_SECRET

CMD ["sh", "-c", "cd /app/bot && gunicorn -w 4 -b 0.0.0.0:8003 main:app"]