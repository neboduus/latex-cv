.PHONY: unit-test-local
unit-test-local:
	env/bin/python3 -m pytest -vv --log-cli-level=DEBUG

.PHONY: unit-test-docker
unit-test-docker:
	docker run unit_test:0.0.1

.PHONY: build-data-ingestor-container
build-data-ingestor-container:
	cd data_ingestor && docker build -t data_ingestor:0.0.1 .

.PHONY: build-it-test-container
build-it-test-container:
	cd it && docker build -t it_test:0.0.1 .

.PHONY: build-unittest-container
build-unittest-container:
	docker build -f unittest.Dockerfile -t unit_test:0.0.1 .

.PHONY: build-containers
build-containers: build-unittest-container build-data-ingestor-container build-it-test-container

.PHONY: create_env
create_env:
	python3.8 -m venv env

.PHONY: install-data-ingestor-requirements
install-data-ingestor-requirements:
	env/bin/pip install -r data_ingestor/requirements.txt

.PHONY: install-etl-pipeline-requirements
install-etl-pipeline-requirements:
	env/bin/pip install -r dags/etl/requirements.txt

.PHONY: init
init: create_env install-etl-pipeline-requirements install-data-ingestor-requirements

.PHONY: deploy
deploy:
	docker-compose up

.PHONY: test-dag
test-dag:
	docker exec airflow-pipeline-airflow-worker-1 airflow dags test etl_pipeline

.PHONY: check-mongo-db
check-mongo-db:
	docker run --network=host it_test:0.0.1

.PHONY: integration-test
integration-test: test-dag check-mongo-db

.PHONY: clean-docker
clean-docker:
	docker-compose down --volumes --remove-orphans
