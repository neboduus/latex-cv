import json
import logging
import os
import datetime
from pathlib import Path

import pandas as pd

from dags.etl.lib import read_data, convert_birthdate, parse_birthdate, clean_text, clean_names, merge_names, calculate_age, \
    calculate_salary_bucket, drop_useless_columns, etl_pipeline

logger = logging.getLogger(__name__)
current_path = Path(os.path.dirname(os.path.realpath(__file__)))


def get_test_resource_as_dict(filename: str) -> dict:
    with open(current_path / 'test_resources' / filename) as file:
        return json.load(file)


def test_read_data():
    employee_data = get_employee_data()
    employee_df = read_data(employee_data)
    assert not employee_df.empty
    column_names = ['EmployeeID', 'FirstName', 'LastName', 'BirthDate', 'Department', 'Salary']
    assert employee_df.columns.to_list() == column_names


def get_employee_data():
    with open(f"{current_path}/data/employee_data.csv") as csv_file:
        employee_data = ''.join(csv_file.readlines())
    return employee_data


def test_parse_birthdate():
    good_birthdate = "1990-08-07"
    bad_birthdate = "xxx-08-07"
    parsed_good_birthdate = parse_birthdate(good_birthdate)
    parsed_bad_birthdate = parse_birthdate(bad_birthdate)
    assert parsed_good_birthdate == datetime.datetime(1990, 8, 7, 0, 0)
    assert pd.isnull(parsed_bad_birthdate)


def test_birthdate_conversion():
    employee_df = convert_birthdate(read_data(get_employee_data()))
    expected_test_resource = "expected_birthdate_column_after_conversion.json"
    expected_birthdate_col_json = get_test_resource_as_dict(expected_test_resource)
    parsed_birthdate_col_json = json.loads(employee_df["ParsedBirthDate"].to_json())
    assert expected_birthdate_col_json == parsed_birthdate_col_json


def test_clean_text():
    texts_test_cases = [
        ("D&Bry", "DBry"),
        ("Elena'00", "Elena00"),
        ('"J"ack "', "Jack"),
        ('Gabriel$   Lakey "', "Gabriel   Lakey")
    ]
    for input_text, expected_output in texts_test_cases:
        output = clean_text(input_text)
        assert output == expected_output


def test_names_cleaning():
    employee_df = read_data(get_employee_data())
    employee_df = clean_names(employee_df)
    expected_test_resource = "expected_firstname_lastname_columns_after_cleaning.json"
    expected_names_cols_json = get_test_resource_as_dict(expected_test_resource)
    parsed_names_cols_json = json.loads(
        employee_df[["FirstName", "LastName"]].to_json(force_ascii=False))
    assert expected_names_cols_json == parsed_names_cols_json


def test_merge_names():
    employee_df = read_data(get_employee_data())
    employee_df = merge_names(employee_df)
    expected_test_resource = "expected_merged_names_columns_after_merging_names.json"
    expected_merged_names_cols_json = get_test_resource_as_dict(expected_test_resource)
    parsed_merged_names_cols_json = json.loads(
        employee_df[["MergedNames"]].to_json(force_ascii=False))
    assert expected_merged_names_cols_json == parsed_merged_names_cols_json


def test_calculate_age():
    employee_df = convert_birthdate(read_data(get_employee_data()))
    employee_df = calculate_age(employee_df)
    expected_test_resource = "expected_age_column_after_calculate_age.json"
    expected_age_col_json = get_test_resource_as_dict(expected_test_resource)
    parsed_age_col_json = json.loads(employee_df[["Age"]].to_json(force_ascii=False))
    assert expected_age_col_json == parsed_age_col_json


def test_calculate_salary_bucket():
    employee_df = read_data(get_employee_data())
    employee_df = calculate_salary_bucket(employee_df)
    expected_test_resource = "expected_salary_bucket_column_after_calculate_age.json"
    expected_salary_bucket_col_json = get_test_resource_as_dict(expected_test_resource)
    parsed_salary_bucket_col_json = json.loads(employee_df[["SalaryBucket"]]
                                               .to_json(force_ascii=False))
    assert expected_salary_bucket_col_json == parsed_salary_bucket_col_json


def test_drop_useless_columns():
    employee_df = read_data(get_employee_data())
    employee_df = drop_useless_columns(employee_df)
    expected_columns = ['EmployeeID', 'Department', 'Salary']
    actual_columns = employee_df.columns.to_list()
    assert expected_columns == actual_columns


def test_elt_pipeline():
    input_data = get_employee_data()
    employee_df = etl_pipeline(input_data)
    expected_test_resource = "expected_etl_pipeline_result.json"
    expected_etl_pipeline_result = get_test_resource_as_dict(expected_test_resource)
    actual_result = json.loads(employee_df.to_json(force_ascii=False))
    assert actual_result == expected_etl_pipeline_result


