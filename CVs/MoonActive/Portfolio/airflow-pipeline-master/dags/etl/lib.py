import json
import logging
from datetime import datetime
from io import StringIO
from typing import Union

import pandas as pd
import pymongo
from pandas._libs import NaTType

logger = logging.getLogger(__name__)


def read_data(data: str, sep: str = ',') -> pd.DataFrame:
    df = pd.read_csv(StringIO(data), sep=sep)
    return df.rename(columns=lambda x: x.strip())


def parse_birthdate(birthdate: str, date_format: str = "%Y-%m-%d") -> Union[datetime, NaTType]:
    try:
        return datetime.strptime(birthdate, date_format)
    except (Exception,):
        return pd.NaT


def convert_birthdate(employee_df: pd.DataFrame) -> pd.DataFrame:
    employee_df['ParsedBirthDate'] = employee_df['BirthDate'].apply(parse_birthdate)
    return employee_df


def clean_text(text: str) -> Union[str, NaTType]:
    replacements_dict = {
        '!': '',
        '@': '',
        '&': '',
        '$': '',
        '"': '',
        '(': '',
        ')': '',
        '.': '',
        '\n': '',
        ';': '',
        '#': '',
        '*': '',
        '_': '',
        "'": '',
        "^": '',
        "=": '',
        # ' ': ''
    }
    try:
        for key, value in replacements_dict.items():
            if key in text:
                text = text.replace(key, value)
        return text.strip()
    except (Exception,):
        return pd.NaT


def clean_names(employee_df: pd.DataFrame) -> pd.DataFrame:
    employee_df['FirstName'] = employee_df['FirstName'].apply(clean_text)
    employee_df['LastName'] = employee_df['LastName'].apply(clean_text)
    return employee_df


def merge_names(employee_df: pd.DataFrame) -> pd.DataFrame:
    employee_df['MergedNames'] = employee_df['FirstName'] + ' ' + employee_df['LastName']
    return employee_df


def calculate_age(employee_df: pd.DataFrame) -> pd.DataFrame:
    today = datetime(2023, 1, 1, 0, 0)
    employee_df['Age'] = employee_df['ParsedBirthDate'] - today
    return employee_df


def categorize_salary(salary: str) -> str:
    try:
        int_salary = int(salary)
        if int_salary < 50000:
            return "A"
        elif 50000 < int_salary < 100000:
            return "B"
        else:
            return "C"
    except (Exception, ):
        return "UNKNOWN"


def calculate_salary_bucket(employee_df: pd.DataFrame) -> pd.DataFrame:
    employee_df['SalaryBucket'] = employee_df['Salary'].map(categorize_salary)
    return employee_df


def drop_useless_columns(employee_df: pd.DataFrame) -> pd.DataFrame:
    return employee_df.drop(columns=['FirstName', 'LastName', 'BirthDate'])


def etl_pipeline(data: str) -> pd.DataFrame:
    employee_df = read_data(data)
    employee_df = convert_birthdate(employee_df)
    employee_df = clean_names(employee_df)
    employee_df = merge_names(employee_df)
    employee_df = calculate_age(employee_df)
    employee_df = calculate_salary_bucket(employee_df)
    employee_df = drop_useless_columns(employee_df)
    return employee_df


def upload_to_mongo(data: pd.DataFrame) -> None:
    mongo_db_client = pymongo.MongoClient("mongodb://mongouser:mongouserpass@mongodb:27017/")
    mongo_db = mongo_db_client["db"]
    etl_pipeline_results = mongo_db["etl_pipeline_results"]
    pipeline_result = json.loads(data.to_json(force_ascii=False))
    etl_pipeline_results.insert_one(pipeline_result)
