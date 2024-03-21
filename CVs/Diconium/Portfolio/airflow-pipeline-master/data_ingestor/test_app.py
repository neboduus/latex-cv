import logging

from data_ingestor.app import current_path

logger = logging.getLogger(__name__)


def test_get_root(client):
    response = client.get("/")
    response_data = response.data.decode('utf-8')
    assert response_data == f"To use this app: http://localhost:5000/data?date=YYYYMMDD"


def test_get_data(client):
    date = "20230623"
    response = client.get(f"/data?date={date}")
    lines = expected_data(date)
    response_data = response.data.decode('utf-8').splitlines()
    assert len(lines) == len(response_data)
    assert lines == response_data


def expected_data(date):
    with open(f"{current_path}/data/{date}_data.csv") as csv_file:
        lines = [
            line.replace('\n', '')
            for line in csv_file.readlines()
        ]
    return lines
