import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import glob
import json
from dotenv import load_dotenv
import os


def make_json(string):
    """
    converts the string representation of a json object into a python dict.
    returns np.nan if the string contains commas.
    """
    try:
        # replace single quotations to make the string represent a JSON object
        json_acceptable_string = string.replace("'", '"')
        return json.loads(json_acceptable_string)
    except:
        # if the string is still not JSON compatible return np.nan
        return np.nan


def unpack(data_frame, column):
    """
    unpacks dict in column to dataframe, preserves index of original dataframe.
    """
    # convert all strings into JSON objects
    unpacked = (
        data_frame[column]
        .apply(make_json)
        .to_frame()
        .rename_axis(index={"id": "kickstarter_id"})
    )

    # unpack json objects and set index
    unpacked_json = pd.json_normalize(unpacked[column]).set_index(unpacked.index)

    # unpack JSON into DataFrame
    return unpacked_json


# get db connection
load_dotenv()
db_connection = os.getenv("KICKSTARTER_DB_URL")

# init database engine
engine = create_engine(db_connection)

# open and read SQL file to create the tables in the 'kickstarter' database
sql = open("create_tables.sql", "r")
sql_file = sql.read()
sql.close()

# execute the SQL to create the empty tables and relations.
engine.execute(sql_file)

# path to each file in the all_data folder
all_paths = glob.glob("raw_data/*.csv")

# list to append df's to
list_of_df = []

# loop through all paths and append each csv as a df
for filename in all_paths:
    df = pd.read_csv(filename, index_col=None, header=0)
    list_of_df.append(df)

# concat all df's into one df
master_df = pd.concat(list_of_df, axis=0, ignore_index=True)

# drop any rows where the id is a duplicate
master_df = master_df.drop_duplicates(subset="id", keep="first")
master_df = master_df.set_index("id")

# define which columns are represented as dicts
unpack_list = ["category", "creator", "location", "photo", "profile", "urls"]

# push master df to DB as the projects table (drop columns containing json objects prior)
master_df.drop(columns=unpack_list).to_sql(
    "kickstarters", engine, if_exists="append", index=True
)

# unpack each column of dicts, place each into SQL DB
for value in unpack_list:
    # perform unpacking of json object
    frame = unpack(master_df, value)

    # push the df to the SQL DB
    frame.to_sql(value, engine, if_exists="append", index=True)
