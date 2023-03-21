FROM apache/airflow:2.5.2
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

#docker build . --tag extending_airflow:latest

#docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler