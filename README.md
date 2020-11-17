# mojap-arrow-pd-parser

A package to provide consistency when loading data into a pandas dataframe.

If you dont really care whether the integer is Int8, Int16 but would just rather know that when loading data the data type will be consistent then this package is for you.

## How to use?

You have a csv file

'''
my_data.csv
'''

and you want to load it into a pandas dataframe using the default data type mapping

'''
my_pandas_df = pa_read_csv_to_pandas('my_data.csv')
'''

and that is it. 

The default behaviour will ensure there is a consistent mapping of the data types.

If you want some control over the default behaviour there are true/false options for each data type.

Data formats currently supported:

- csv
- jsonl

## What is the default behaviour for mapping datatypes?

|  Arrow data type | Pandas data type |
|------------------|------------------|
| intX, uintX      | Int64Dtype       |
| string           | StringDtype      |
| bool             | BooleanDtype     |


