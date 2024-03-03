import pyodbc
import json
import re
def fetch_data_as_list_of_dicts(records):
    columns = [column[0] for column in records.description]
    result_set = records.fetchall()

    list_of_dicts = []
    for row in result_set:
        row_dict = dict(zip(columns, row)) #zip() used to pair up the column name with value , dict() makes it into dictionary format
        list_of_dicts.append(row_dict)

    return list_of_dicts

def format_datetime(date_time):
    # Define the pattern to keep
    pattern = r'[0-9\-:]+'

    # Find all matches in the text
    matches = re.findall(pattern, date_time)

    # Concatenate matches into a single string
    result = ' '.join(matches)

    return result