import json
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))


def get_test_case(test_case: str) -> dict:
    file_name = f'{test_case}_test_case.json'
    with open(current_path / 'resources' / file_name) as file:
        return json.load(file)
