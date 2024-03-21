import logging

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonVirtualenvOperator


args = {
    'owner': 'marian',
    'start_date': days_ago(1)
}

logger = logging.getLogger(__name__)

dag = DAG(dag_id='etl_pipeline',
          default_args=args,
          schedule_interval=None,
          is_paused_upon_creation=True)


def process_etl_pipeline():
    import requests
    from etl.lib import etl_pipeline, upload_to_mongo

    url = "http://data-ingestor:5000/data?date=20230623"
    response = requests.get(url)
    data = response.content.decode('utf-8')
    pipeline_result = etl_pipeline(data)
    print("---------------RESULT--------------")
    print(pipeline_result)
    upload_to_mongo(pipeline_result)


with dag:
    read_data = PythonVirtualenvOperator(
        task_id="read_data_step",
        requirements=[
            "requests==2.31.0",
            "pandas==1.3.5",
            "pymongo==4.4.0"
        ],
        python_callable=process_etl_pipeline,
    )

    read_data
