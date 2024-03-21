import json
import os
from pathlib import Path

import pymongo

current_path = Path(os.path.dirname(os.path.realpath(__file__)))


def read_json_as_dict(path: str) -> dict:
    with open(current_path / path) as f:
        return json.load(f)


if __name__ == '__main__':
    mongo_db_client = pymongo.MongoClient("mongodb://mongouser:mongouserpass@mongodb:27017/")
    mongo_db = mongo_db_client["db"]
    etl_pipeline_results = mongo_db["etl_pipeline_results"]
    data = [x for x in etl_pipeline_results.find({})]
    assert len(data) != 0, "Mongo does not contain expected Data. IT FAILED."
    data = data[0]
    del data["_id"]
    expected_data = read_json_as_dict('expected_mongo_content.json')
    assert data == expected_data, "Mongo does not contain expected Data. IT FAILED."
    print("Mongo contains expected data. IT PASSED.")
