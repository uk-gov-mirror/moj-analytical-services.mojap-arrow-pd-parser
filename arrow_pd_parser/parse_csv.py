import pandas as pd
import pyarrow as pa
from pyarrow import csv

def pa_read_csv(csv_path, test_col_types):
    csv_co = csv.ConvertOptions(column_types=test_col_types)
    pa_csv_table = csv.read_csv(csv_path, convert_options = csv_co)
    return pa_csv_table


def pa_to_pd(arrow_table, new_int_type: bool = True):
    if new_int_type:
        return arrow_table.to_pandas(timestamp_as_object=True) # Some parameters
    else:
        return arrow_table.to_pandas(timestamp_as_object=True) # Some parameters


def pa_read_csv_to_pandas(csv_path, test_col_types, new_int_type: bool = True):
    arrow_table = pa_read_csv(csv_path, test_col_types)
    return pa_to_pd(arrow_table, new_int_type=new_int_type)