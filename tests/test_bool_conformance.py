import pytest
import pyarrow as pa

from arrow_pd_parser.parse import pa_read_csv_to_pandas


@pytest.mark.parametrize(
    "col_name,pd_old_type,pd_new_type",
    [("my_bool", "bool", "boolean"), ("my_nullable_bool", "object", "boolean")],
)

def pa_read_csv(csv_path, test_col_types):
    csv_co = csv.ConvertOptions(column_types=test_col_types)
    pa_csv_table = csv.read_csv(csv_path, convert_options=csv_co)
    return pa_csv_table

arrow_table = pa_read_csv("tests/data/bool_type.csv", test_col_types)


arrow_table.to_pandas(
            timestamp_as_object=True, types_mapper={pa.bool_(): boolObjectDtype()}.get
        )

def test_bool(col_name, pd_old_type, pd_new_type):
    test_col_types = {"bool_col": getattr(pa, "bool_")()}
    df_old = arrow_to_pandas(
        "tests/data/bool_type.csv", test_col_types, pd_boolean=False
    )
    assert str(df_old[col_name].dtype) == pd_old_type

    df_new = arrow_to_pandas(
        "tests/data/bool_type.csv", test_col_types, pd_boolean=True
    )
    assert str(df_new[col_name].dtype) == pd_new_type
