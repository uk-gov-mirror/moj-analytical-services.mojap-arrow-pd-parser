import os
import pyarrow as pa

from arrow_pd_parser.parse import pa_read_csv_to_pandas
from arrow_pd_parser.export import pd_to_csv, pd_to_json
from pandas.testing import assert_frame_equal

schema = pa.schema(
    [
        ("i", pa.int64()),
        ("my_bool", pa.bool_()),
        ("my_nullable_bool", pa.bool_()),
        ("my_date", pa.date32()),
        ("my_datetime", pa.timestamp("s")),
        ("my_int", pa.int64()),
        ("my_string", pa.string()),
    ]
)


def test_pd_to_csv():
    imported = pa_read_csv_to_pandas("tests/data/all_types.csv", schema)

    try:
        pd_to_csv(imported, "tests/data/export_test.csv", schema)
        reimported = pa_read_csv_to_pandas("tests/data/export_test.csv", schema)
        assert_frame_equal(imported, reimported)

    finally:
        os.remove("tests/data/export_test.csv")


def test_pd_to_json():
    imported = pa_read_csv_to_pandas("tests/data/all_types.csv", schema)

    try:
        pd_to_json(imported, "tests/data/export_test.json", schema)
        reimported = pa_read_csv_to_pandas("tests/data/export_test.json", schema)
        assert_frame_equal(imported, reimported)

    finally:
        os.remove("tests/data/export_test.json")
