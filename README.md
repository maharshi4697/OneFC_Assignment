# OneFC_Assignment

The Python Script, 'Assignment.py' uses a CSV file as an input. Performs transformations on the data as per a JSON Schema and outputs 2 files, 1 for the Correct Output and another for the errors in the input data file.

To Run the following code, the following steps need to performed.

1. Create a Virtual Env with the following command.
	   virtualenv OneFCenv -p python3.7

2. Enter The Virtual Environment with the following command.
	   source OneFCenv/bin/activate

3. Install all the requirements to run the python file using the following command.
	   pip install -r Requirements.txt

4. Run the python file using the following command.
	   python Assignment.py

5. After the previous command is run, enter the details as prompted in the terminal.Upon confusion, the following command can be run.
    python Assignment.py --help


To generate the error json, use 'data_new.csv' instead of 'data.csv'
and use 'schema.json'. 'schema_new.json' will not work for 'Assignment.py',
'schema_new.json' is meant to used with 'Assignment_New.py'



The Python Script, 'Assignment_New.py' is a more optimized form of 'Assignment.py'. To run this code, use the Json schema, 'schema_new.json' instead of 'schema.json'. The schema_new.json has been modified to verify patterns using the schema instead of hard coding it. The benefit is that only 1 source of truth needs to be maintained and everytime something needs to be changed, the code doesn't need to be changed, only the 'schema_new.json' should be modified.



To run the python script 'Assignment_New.py' repeat the above steps (1-3).

4. Run the python file using the following command.
		python Assignment.py

5. In the prompt, enter json path of 'schema_new.json'. In order to generate errors.json, use the 'data_new.csv' instead of 'data.csv'
