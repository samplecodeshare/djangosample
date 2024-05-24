from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import YamlForm
import yaml
import os
import yaml
from django.shortcuts import render, get_object_or_404
from django.conf import settings

def list_yaml_files(request):
    files_data = []
    for filename in os.listdir(settings.YAML_FILES_DIR):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            with open(os.path.join(settings.YAML_FILES_DIR, filename), 'r') as file:
                content = yaml.safe_load(file)
                files_data.append({
                    'id': content.get('id'),
                    'title': content.get('info', {}).get('title'),
                    'version': content.get('info', {}).get('version'),
                    'owner': content.get('info', {}).get('owner'),
                    'domain': content.get('info', {}).get('domain'),
                    'filename': filename
                })
    return render(request, 'list_yaml_files.html', {'files_data': files_data})

def edit_yaml(request):
    filename = request.GET.get('filename')
    file_path = os.path.join(settings.YAML_FILES_DIR, filename)
    with open(file_path, 'r') as file:
        yaml_content = file.read()

    if request.method == 'POST':
        form = YamlForm(request.POST)
        if form.is_valid():
            with open(filename, 'w') as file:
                yaml_content = form.cleaned_data['yaml_content']
                yaml_content = "\n".join([line.rstrip() for line in yaml_content.splitlines()])
                file.write(yaml_content)
            return redirect('display_yaml', filename=filename)
    else:
        form = YamlForm(initial={'yaml_content': yaml_content})

    return render(request, 'edit_yaml.html', {'form': form})


def display_yaml(request, filename):
    file_path = os.path.join(settings.YAML_FILES_DIR, filename)
    print(str(file_path))
    with open(file_path, 'r') as file:
         yaml_content = yaml.safe_load(file)
    context = {
        'data': yaml_content,
        'filename' : filename
    }

    return render(request, 'display_yaml.html', context )