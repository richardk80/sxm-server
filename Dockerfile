# https://hub.docker.com/_/python
FROM python:3.10.1

WORKDIR .
COPY . .

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 3 --timeout 3600 --threads 8 main:api