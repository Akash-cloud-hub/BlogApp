import pyodbc
import json
def fetch_data_as_list_of_dicts(records):
    columns = [column[0] for column in records.description]
    result_set = records.fetchall()

    list_of_dicts = []
    for row in result_set:
        row_dict = dict(zip(columns, row)) #zip() used to pair up the column name with value , dict() makes it into dictionary format
        list_of_dicts.append(row_dict)

    return list_of_dicts