# This file extracts raw data from MySQL database

import pandas as pd  # data manipulation library
from sqlalchemy import create_engine  # database connection engine
from dotenv import load_dotenv  # load environment variables from .env file
from pathlib import Path
import os  # access environment variables

load_dotenv()  # load .env file variables into environment


def get_dataset_path():
    dataset_path = os.getenv('DATASET_PATH')
    if not dataset_path:
        return None
    dataset_path = os.path.expandvars(dataset_path)
    dataset_path = os.path.expanduser(dataset_path)
    return Path(dataset_path)


def get_engine():
    # build mysql connection string using env variables
    url = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(url)  # return sqlalchemy engine object

def extract_data():
    dataset_path = get_dataset_path()
    if dataset_path is not None:
        if dataset_path.exists():
            print(f"Loading dataset from CSV: {dataset_path}")
            df = pd.read_csv(dataset_path)
            print(f"Loaded {len(df)} rows from CSV dataset")
            return df
        raise FileNotFoundError(f"DATASET_PATH is set to '{dataset_path}', but the file does not exist.")

    engine = get_engine()  # get database connection
    df = pd.read_sql("SELECT * FROM online_shoppers", engine)  # fetch all rows from table
    print(f"Extracted {len(df)} rows")  # log how many rows fetched
    return df  # return dataframe

if __name__ == "__main__":
    df = extract_data()  # run extraction
    print(df.head())  # print first 5 rows to verify