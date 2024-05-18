import os
import yaml
import json

def read_metadata_file(file_path):
    """Reads a YAML file and returns its content as a Python dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_metadata_from_directories(base_directory):
    """Iterates through directories and reads metadata.yml files."""
    json_list = []
    
    for root, dirs, files in os.walk(base_directory):
        if 'metadata.yml' in files:
            file_path = os.path.join(root, 'metadata.yml')
            try:
                yaml_content = read_metadata_file(file_path)
                json_list.append(yaml_content)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return json_list

def main():
    base_directory = '/path/to/your/directories'  # Replace with your base directory path
    metadata_json_list = get_metadata_from_directories(base_directory)
    
    # Optionally, print or save the list of JSON objects
    print(json.dumps(metadata_json_list, indent=2))

if __name__ == "__main__":
    main()
