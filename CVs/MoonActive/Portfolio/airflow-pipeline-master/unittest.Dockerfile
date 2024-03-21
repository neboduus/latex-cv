FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY data_ingestor/requirements.txt data_ingestor_requirements.txt
COPY dags/etl/requirements.txt etl_requirements.txt
RUN pip3 install -r data_ingestor_requirements.txt
RUN pip3 install -r etl_requirements.txt

COPY . .

CMD ["python3", "-m", "pytest", "-vv", "--log-cli-level=DEBUG"]
