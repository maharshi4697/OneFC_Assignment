#Importing all the required libraries.
from jsonschema import validate
from collections import OrderedDict
import json
import csv
import pandas as pd
import click
import re

#Defining all input and output paths.
def paths(csv_path,schema_path,output_path,error_path):
    csv_file_path = csv_path
    json_schema_path= schema_path
    json_output_path= output_path
    json_error_path= error_path
    return csv_file_path,json_schema_path,json_output_path,json_error_path

#Reading the JSON schema.
def read_json_schema(path):
    with open(path,'r') as f:
        schema = json.load(f)
    return schema

#Reading the input data csv.
def read_csv(path):
    df=pd.read_csv(path)
    return df

#Transforming the input data according to the JSON schema.
def transformations(df,schema):
    df.columns = schema['properties'].keys()
    df.iloc[:, 0]=df.iloc[:, 0].apply(str)
    df_out=df.to_dict(into=OrderedDict,orient='index')
    return df_out

#Running Regex Commands for Data Validation. Better alternative is to use Pattern in the JSON Schema
def data_validation(df):
    person_id_pattern=re.compile(r'^[0-9]+$')
    date_pattern=re.compile(r'^([1-9]|[1][0-2])[/]([1-9]|[1,2]\d|[3][0,1])[/](\d\d)\s([1]{0,1}\d|[2][0-3])[:]([0-5]\d)+$')
    floor_access_pattern=re.compile(r'^\d{0,1}\d{1}$')
    building_pattern=re.compile(r'^[A-C]$')
    error_row=[]
    error_column=[]
    col1=[]
    col2=[]
    col3=[]
    col4=[]
    for i in df:
        if(re.search(person_id_pattern,list(df[i].values())[0]))==None:
            error_row.append(df[i])
            error_column.append(list(df[i].keys())[0])
        elif(re.search(date_pattern,list(df[i].values())[1]))==None:
            error_row.append(df[i])
            error_column.append(list(df[i].keys())[1])
        elif(re.search(floor_access_pattern,str(list(df[i].values())[2])))==None:
            error_row.append(json.dumps(df[i]))
            error_column.append(list(df[i].keys())[2])
        elif(re.search(building_pattern,list(df[i].values())[3]))==None:
            error_row.append(json.dumps(df[i]))
            error_column.append(list(df[i].keys())[3])
        else:
            col1.append(list(df[i].values())[0])
            col2.append(list(df[i].values())[1])
            col3.append((list(df[i].values())[2]))
            col4.append(list(df[i].values())[3])
    correct_df=pd.DataFrame({list(df[0].keys())[0]:col1,list(df[i].keys())[1]:col2,list(df[0].keys())[2]:col3,list(df[i].keys())[3]:col4})
    correct=correct_df.to_dict(into=OrderedDict,orient='index')
    error_df=pd.DataFrame({'error_row':error_row,'error_column':error_column})
    if error_df.empty==False:
        errors=error_df.to_dict(into=OrderedDict,orient='index')
        return correct,errors
    else:
        return correct,None

#Validating the resultant data against the schema for validation.
def schema_validation(df,schema):
    error_row=[]
    error_column=[]
    for i in df:
        try:
            validate(instance=df[i], schema=schema)
        except Exception as e:
            error_row.append(df[i])
            error_column.append(e, "Occured at ",df[i])
    error_df=pd.DataFrame({'error_row':error_row,'error_column':error_column})
    if error_df.empty==False:
        errors=error_df.to_dict(into=OrderedDict,orient='index')
        return errors

#Output the Json files.
def output_json(df,path):
    output_file = open(path, 'w', encoding='utf-8')
    for i in df:
        json.dump(df[i], output_file, indent=4)
        output_file.write("\n")

#Click is used for input in the terminal.
@click.command()
@click.option('--csv_path', prompt='Enter CSV File Path', help='This is the csv file path to validate.')
@click.option('--schema_path', prompt='Enter JSON Schema Path', help='This is the json schema path to validate.')
@click.option('--output_path', prompt='Enter JSON Output Path', help='This is the json output path after validation.')
@click.option('--error_path', prompt='Enter Errors JSON Output Path', help='This is the json output path after validation.')
def run(csv_path,schema_path,output_path,error_path):
    csv_file_path = csv_path
    json_schema_path = schema_path
    json_output_path = output_path
    json_error_path = error_path
    csv_file_path,json_schema_path,json_output_path,json_error_path=paths(csv_file_path,json_schema_path,json_output_path,json_error_path)
    json_schema=read_json_schema(json_schema_path)
    input_df=read_csv(csv_file_path)
    df_transform=transformations(input_df,json_schema)
    correct,errors_data=data_validation(df_transform)
    errors_schema=schema_validation(correct,json_schema)
    if errors_data is not None and errors_schema is not None:
        errors_data.update(errors_schema)
        errors=errors_data
    elif errors_data is None and errors_schema is not None:
        errors=errors_schema
    elif errors_schema is None and errors_schema is None:
        errors=errors_data
    output_json(correct,json_output_path)
    if errors!=None:
        output_json(errors,json_error_path)

#Main Function
if __name__ == "__main__":
    run()
