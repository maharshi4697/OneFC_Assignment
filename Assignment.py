# Importing all the required libraries.
import json
from collections import OrderedDict
import re
import click
import pandas as pd
from jsonschema import validate

# Defining all input and output paths.
def paths(csv_path, schema_path, output_path, error_path):
    csv_file_path = csv_path
    json_schema_path = schema_path
    json_output_path = output_path
    json_error_path = error_path
    return csv_file_path, json_schema_path, json_output_path, json_error_path

# Reading the JSON schema.
def read_json_schema(path):
    with open(path, 'r') as f:
        schema = json.load(f)
    return schema

# Reading the input data csv.
def read_csv(path):
    df = pd.read_csv(path)
    return df

# Transforming the input data according to the JSON schema.
def transformations(df, schema):

    # Removing old column names and assigning new column names as per schema.
    df.columns = schema['properties'].keys()

    # Changing data type of first column for integer to string.
    df.iloc[:, 0] = df.iloc[:, 0].apply(str)

    # Converting DataFrame to Ordered Dict to pass it in json string format.
    df_out = df.to_dict(into=OrderedDict, orient='index')
    return df_out


# Running Regex Commands for Data Validation.
# Better alternative is using Pattern in the JSON Schema
# Demonstration done in Assignment_New.py invoking Schema_New.json
def data_validation(df):

    # Assigning Regex patterns for all the columns to validate.
    person_id_pattern = re.compile(r'^[0-9]+$')
    date_pattern = re.compile(r'^([1-9]|[1][0-2])[/]([1-9]|[1,2]\d|[3][0,1])[/](\d\d)\s([1]{0,1}\d|[2][0-3])[:]([0-5]\d)+$')
    floor_access_pattern = re.compile(r'^\d{0,1}\d{1}$')
    building_pattern = re.compile(r'^[A-C]$')

    # Errors are going to be stored in these 2 lists, will later be converted to Ordered Dict.
    error_row = []
    error_column = []

    # Correct columns are going to stored in these 4 lists, will later be converted to Ordered Dict.
    col1 = []
    col2 = []
    col3 = []
    col4 = []

    # Accessing all the data.
    for i in df:

        # If person_id doesn't match, then store the error and the column value.
        if(re.search(person_id_pattern, list(df[i].values())[0])) is None:
            error_row.append(df[i])
            error_column.append(list(df[i].keys())[0])

        # If date_pattern doesn't match, then store the error and the column value.
        elif(re.search(date_pattern, list(df[i].values())[1])) is None:
            error_row.append(df[i])
            error_column.append(list(df[i].keys())[1])

        # If floor_access_pattern doesn't match, then store the error and the column value.
        elif(re.search(floor_access_pattern, str(list(df[i].values())[2]))) is None:
            error_row.append(json.dumps(df[i]))
            error_column.append(list(df[i].keys())[2])

        # If building_pattern doesn't match, then store the error and the column value.
        elif(re.search(building_pattern, list(df[i].values())[3])) is None:
            error_row.append(json.dumps(df[i]))
            error_column.append(list(df[i].keys())[3])

        # Store all the correct values in lists.
        else:
            col1.append(list(df[i].values())[0])
            col2.append(list(df[i].values())[1])
            col3.append(list(df[i].values())[2])
            col4.append(list(df[i].values())[3])

    # Correct Lists are first converted to DataFrame and then finally OrderedDict
    correct_df = pd.DataFrame({list(df[0].keys())[0]:col1,
                               list(df[1].keys())[1]:col2,
                               list(df[2].keys())[2]:col3,
                               list(df[3].keys())[3]:col4})
    correct = correct_df.to_dict(into=OrderedDict, orient='index')

    # Error Lists are first converted to DataFrame.
    error_df = pd.DataFrame({'error_row':error_row,
                             'error_column':error_column})

    # If Errors exist,then are converted to OrderedDict and returned.
    # Else None is returned along with the correct list.
    if error_df.empty is False:
        errors = error_df.to_dict(into=OrderedDict, orient='index')
        return correct, errors
    else:
        return correct, None

# Validation of the input against the schema.
def schema_validation(df, schema):

    # Errors are going to be stored in these 2 lists, will later be converted to Ordered Dict.
    error_row = []
    error_column = []

    # Correct columns are going to stored in these 4 lists, will later be converted to Ordered Dict.
    col1 = []
    col2 = []
    col3 = []
    col4 = []

    # Accessing all the data.
    for i in df:
        try:
            # If validation is correct and matches then None is returned.
            if validate(instance=df[i], schema=schema) is None:
                #Appending the corresponding correct values in lists.
                col1.append(list(df[i].values())[0])
                col2.append(list(df[i].values())[1])
                col3.append((list(df[i].values())[2]))
                col4.append(list(df[i].values())[3])

        except Exception as e:
            # The errors rows and their corresponding messages are appended in the following list
            error_row.append(df[i])
            error_column.append(json.dumps(e.message))

    # Correct Lists are first converted to DataFrame and then finally OrderedDict.
    correct_df = pd.DataFrame({list(df[0].keys())[0]:col1,
                               list(df[1].keys())[1]:col2,
                               list(df[2].keys())[2]:col3,
                               list(df[3].keys())[3]:col4})
    correct = correct_df.to_dict(into=OrderedDict, orient='index')

    # Error Lists are first converted to DataFrame.
    error_df = pd.DataFrame({'error_row':error_row,
                             'error_column':error_column})

    # If Errors exist,then are converted to OrderedDict and returned.
    # Else None is returned along with the correct list.
    if error_df.empty is False:
        errors = error_df.to_dict(into=OrderedDict, orient='index')
        return correct, errors
    else:
        return correct, None

# Output the Json files.
def output_json(df, path):
    output_file = open(path, 'w', encoding='utf-8')
    for i in df:
        json.dump(df[i], output_file, indent=4)
        output_file.write("\n")

#Click is used for input in the terminal.
@click.command()
@click.option('--csv_path', prompt='Enter CSV File Path',
              help='This is the csv file path to validate.')
@click.option('--schema_path', prompt='Enter JSON Schema Path',
              help='This is the json schema path to validate.')
@click.option('--output_path', prompt='Enter JSON Output Path',
              help='This is the json output path after validation.')
@click.option('--errors_path', prompt='Enter Errors JSON Output Path',
              help='This is the json output path after validation.')
def run(csv_path, schema_path, output_path, errors_path):

    # Set input and output paths.
    csv_file_path = csv_path
    json_schema_path = schema_path
    json_output_path = output_path
    errors_output_path = errors_path
    csv_file_path, json_schema_path, json_output_path, errors_output_path = paths(csv_file_path, json_schema_path, json_output_path, errors_output_path)

    # Read the input files.
    json_schema = read_json_schema(json_schema_path)
    input_df = read_csv(csv_file_path)

    # Transform the input csv based on json schema.
    df_transform = transformations(input_df, json_schema)

    # Perform data validation for the datausing regex.
    correct_data, errors_data = data_validation(df_transform)

    # Perform schema validation for the data using json schema.
    correct_schema, errors_schema = schema_validation(correct_data, json_schema)

    #Append Errors of Data Validation and Schema Validation Together
    if errors_data is not None and errors_schema is not None:
        errors_data.update(errors_schema)
        errors = errors_data
    elif errors_data is None and errors_schema is not None:
        errors = errors_schema
    elif errors_schema is None and errors_schema is None:
        errors = errors_data

    # Output jsons.
    output_json(correct_schema, json_output_path)
    if errors is not None:
        output_json(errors, errors_output_path)

#Main Function
if __name__ == "__main__":
    run()
