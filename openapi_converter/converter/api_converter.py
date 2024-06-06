import json
from ruamel.yaml import YAML
from collections import OrderedDict
import re
import io

def generate_openapi_spec_from_json_string(json_string):
    sample_json = json.loads(json_string, object_pairs_hook=OrderedDict)
    return generate_openapi_spec_from_json(sample_json)

def generate_openapi_spec_from_json(sample_json):
    components = OrderedDict({"schemas": OrderedDict()})
    paths = OrderedDict()

    for key, value in sample_json.items():
        schema_name = key.capitalize()
        components["schemas"][schema_name] = generate_schema(value)
        paths[f"/{key}"] = OrderedDict({
            "get": {
                "summary": f"Get {key}",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{schema_name}"
                                }
                            }
                        }
                    }
                }
            }
        })

    return OrderedDict({
        "openapi": "3.0.0",
        "info": OrderedDict({
            "title": "Generated API",
            "version": "1.0.0"
        }),
        "paths": paths,
        "components": components
    })

def generate_schema(value):
    if isinstance(value, dict):
        return OrderedDict({
            "type": "object",
            "properties": OrderedDict({k: generate_schema(v) for k, v in value.items()})
        })
    elif isinstance(value, list):
        if len(value) > 0:
            return OrderedDict({
                "type": "array",
                "items": generate_schema(value[0])
            })
        else:
            return OrderedDict({
                "type": "array",
                "items": OrderedDict()
            })
    elif isinstance(value, str):
        return OrderedDict({
            "type": "string",
            **infer_string_format(value)
        })
    elif isinstance(value, int):
        return OrderedDict({
            "type": "integer",
            "minimum": value,
            "maximum": value
        })
    elif isinstance(value, float):
        return OrderedDict({
            "type": "number",
            "minimum": value,
            "maximum": value
        })
    elif isinstance(value, bool):
        return OrderedDict({"type": "boolean"})
    else:
        return OrderedDict({"type": "string"})

def infer_string_format(value):
    # Define patterns for different string formats
    patterns = {
        "date-time": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
        "email": r"^[\w\.-]+@[\w\.-]+\.\w+$",
        "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
    }
    for fmt, pattern in patterns.items():
        if re.match(pattern, value):
            return {"format": fmt}
    return {}

def convert_ordered_dict_to_dict(obj):
    if isinstance(obj, OrderedDict):
        return {k: convert_ordered_dict_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ordered_dict_to_dict(i) for i in obj]
    else:
        return obj

def get_openapi_spec_yaml(input):
    openapi_spec = generate_openapi_spec_from_json_string(input)
    yaml = YAML()
    yaml.default_flow_style = False
    # Convert OrderedDict to dict before dumping YAML
    openapi_spec_dict = convert_ordered_dict_to_dict(openapi_spec)
    output = io.StringIO()
    yaml.dump(openapi_spec_dict, output)
    yaml_str = output.getvalue()
    return yaml_str
