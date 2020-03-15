from jsonschema import validate
from collections import OrderedDict
import json
import csv
import pandas as pd
import click


def paths(csv_path,schema_path,output_path):
    csv_file_path = csv_path
    json_schema_path= schema_path
    json_output_path= output_path
    return csv_file_path,json_schema_path,json_output_path

def read_json_schema(path):
    with open(path,'r') as f:
        schema = json.load(f)
    return schema

def read_csv(path):
    df=pd.read_csv(path)
    return df

def transformations(df,schema):
    df.columns = schema['properties'].keys()
    df.iloc[:, 0]=df.iloc[:, 0].apply(str)
    df_out=df.to_dict(into=OrderedDict,orient='index')
    return df_out

def validation(df,schema):
    for i in df:
        validate(instance=df[i], schema=schema)

def output_json(df,path):
    output_file = open(path, 'w', encoding='utf-8')
    for i in df:
        json.dump(df[i], output_file, indent=4)
        output_file.write("\n")

@click.command()
@click.option('--csv_path', prompt='Enter CSV File Path', help='This is the csv file path to validate.')
@click.option('--schema_path', prompt='Enter JSON Schema Path', help='This is the json schema path to validate.')
@click.option('--output_path', prompt='Enter JSON Output Path', help='This is the json output path after validation.')
def run(csv_path,schema_path,output_path):
    csv_file_path = csv_path
    json_schema_path = schema_path
    json_output_path = output_path
    csv_file_path,json_schema_path,json_output_path=paths(csv_file_path,json_schema_path,json_output_path)
    json_schema=read_json_schema(json_schema_path)
    input_df=read_csv(csv_file_path)
    df=transformations(input_df,json_schema)
    validation(df,json_schema)
    output_json(df,json_output_path)

if __name__ == "__main__":
    run()
