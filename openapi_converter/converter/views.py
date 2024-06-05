# SELECT 
#     order_id, 
#     order_timestamp, 
#     order_total, 
#     customer_id, 
#     customer_email_address, 
#     processed_timestamp
# FROM 
#     orders
# FOR JSON AUTO, ROOT('orders')

import pyodbc
import json
import yaml
from collections import OrderedDict
from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm

def connect_to_db(connection_string):
    conn = pyodbc.connect(connection_string)
    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return columns, rows

def generate_json_schema(columns, rows):
    def get_type(value):
        if isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, str):
            return "string"
        else:
            return "null"
    
    schema = OrderedDict({
        "type": "object",
        "properties": OrderedDict()
    })

    for column in columns:
        example_value = rows[0][columns.index(column)] if rows else None
        column_type = get_type(example_value)
        
        schema["properties"][column] = {
            "type": column_type
        }

        if column_type == "string":
            schema["properties"][column]["minLength"] = len(example_value)
            schema["properties"][column]["maxLength"] = len(example_value)
            if '@' in example_value:
                schema["properties"][column]["format"] = "email"
            if '-' in example_value and len(example_value) == 36:
                schema["properties"][column]["format"] = "uuid"
                
    return schema

def jsonschema_to_openapi(json_schema, title="API Schema", version="1.0.0"):
    openapi_template = {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version
        },
        "paths": {},
        "components": {
            "schemas": {
                "Example": json_schema
            }
        }
    }
    return openapi_template

def convert_input(input_type, content):
    if input_type == 'sql':
        # Simulating database connection and execution
        # Replace with actual connection string and query execution
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_db;UID=your_user;PWD=your_password'
        conn = connect_to_db(connection_string)
        columns, rows = execute_query(conn, content)
        json_schema = generate_json_schema(columns, rows)
    
    elif input_type == 'json':
        json_content = json.loads(content)
        json_schema = json.loads(json.dumps(json_content), object_pairs_hook=OrderedDict)
    
    elif input_type == 'xml':
        import xmltodict
        json_content = xmltodict.parse(content)
        json_schema = json.loads(json.dumps(json_content), object_pairs_hook=OrderedDict)
    
    openapi_spec = jsonschema_to_openapi(json_schema)
    return openapi_spec

def input_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input_type = form.cleaned_data['input_type']
            content = form.cleaned_data['content']
            openapi_spec = convert_input(input_type, content)
            openapi_yaml = yaml.dump(openapi_spec, sort_keys=False)
            return HttpResponse(openapi_yaml, content_type="application/x-yaml")
    else:
        form = InputForm()
    
    return render(request, 'converter/input.html', {'form': form})
