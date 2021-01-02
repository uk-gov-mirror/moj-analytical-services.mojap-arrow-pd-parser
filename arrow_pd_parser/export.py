import pandas as pd
import pyarrow as pa

from typing import Union, IO


def conform_copy(df: pd.DataFrame, schema: pa.Schema):
    """Make a copy of a dataframe with its columns adjusted to match a schema.

    Args:
        df (pd.DataFrame): a pandas dataframe
        schema (pa.Schema): a pyarrow schema that matches the dataframe
    """
    new = df.copy()
    for col in new.columns:
        if schema.field(col).type in [pa.date32(), pa.date64()]:
            new[col] = pd.to_datetime(new[col]).dt.strftime("%Y-%m-%d")
        elif schema.field(col).type == pa.timestamp("s"):
            new[col] = pd.to_datetime(new[col]).dt.strftime("%Y-%m-%d %H:%M:%S")
        elif schema.field(col).type == pa.timestamp("ms"):
            # Truncates microseconds rather than rounding - acceptable error?
            new[col] = (
                pd.to_datetime(new[col]).dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]
            )
        elif schema.field(col).type == pa.timestamp("us"):
            new[col] = pd.to_datetime(new[col]).dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif schema.field(col).type == pa.timestamp("ns"):
            # Make string as microseconds, then get nanosecond and append to the end
            # NaN get read as floats, so fill NaN with 0, then convert to int and string
            # Seems overcomplicated - is there a better way?
            new[col] = pd.to_datetime(new[col]).dt.strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ) + new[col].dt.nanosecond.fillna(0).astype(int).astype(str).str.zfill(3)
    return new


def pd_to_csv(
    df: pd.DataFrame,
    output_file: Union[IO, str],
    schema: Union[pa.Schema, None] = None,
    index=False,
    **kwargs,
):
    """Make a dataframe conform to an Arrow schema, then export it to csv.

    Args:
        df (pd.DataFrame): a pandas dataframe
        output_file (IO or str): the path you want to export to
        schema (pa.Schema): a pyarrow schema that matches the dataframe
        index (bool): standard pandas .to_csv index argument, but defaulting to False
        **kwargs: any other keyword arguments to pass to pandas .to_csv
    """
    # possibly move the 'if schema' stuff into a conform function
    if schema:
        new = conform_copy(df, schema)
    else:
        new = df

    new.to_csv(output_file, index=index, **kwargs)


def pd_to_json(
    df: pd.DataFrame,
    output_file: Union[IO, str],
    schema: Union[pa.Schema, None] = None,
    index=False,
    orient="records",
    lines=True,
    indent=4,
    **kwargs,
):
    """Make a dataframe conform to an Arrow schema, then export it to json newline.

    Args:
        df (pd.DataFrame): a pandas dataframe
        output_file (IO or str): the path you want to export to
        schema (pa.Schema): a pyarrow schema that matches the dataframe
        index (bool): standard pandas .to_json index argument, but defaulting to False
        orient (str): standard pandas .to_json orient argument, defaulting to 'records'
        lines (bool): standard pandas .to_json lines argument, defaulting to True
        **kwargs: any other keyword arguments to pass to pandas .to_json
    """
    if schema:
        new = conform_copy(df, schema)
    else:
        new = df

    new.to_json(output_file, index, orient, lines, indent, **kwargs)
