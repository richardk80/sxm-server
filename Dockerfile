# https://hub.docker.com/_/python
FROM python:3.13.1-alpine

WORKDIR /app
COPY . .

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "--timeout", "3600", "main:app"]
