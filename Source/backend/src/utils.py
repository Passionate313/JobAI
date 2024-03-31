import os
from datetime import datetime
from bson import ObjectId

def object_id_str(value: ObjectId):
    return str(value)


def get_year_from_date_string(date_string: str):
    """Gets year value from date string formatted like YYYY-MM-DD"""
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    year = date_object.year
    return str(year)


def delete_file(file_path):
    """
    Deletes a file at the specified path.
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted successfully")
        else:
            print("Error: %s file not found" % file_path)
    except Exception as e:
        print(e)


def get_first_value_of_list(string_list: list[str]):
    if len(string_list):
        return string_list[0]
    else:
        return None
