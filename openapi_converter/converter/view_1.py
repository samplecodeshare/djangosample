import pyodbc
import json
import yaml
from collections import OrderedDict
from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm,OpenAPIGeneratorForm
from .openapi_generator import get_openapi_spec_yaml

def input_view(request):
    if request.method == 'POST':
        form = OpenAPIGeneratorForm(request.POST)
        sample_json = request.POST.get('json_sample')
        try:
            openapi_spec = get_openapi_spec_yaml(sample_json)
            # print(openapi_spec)
        except json.JSONDecodeError:
            openapi_spec = {"error": "Invalid JSON"}
        context = {
            'form': form,
            'openapi_spec': openapi_spec
        }
        return render(request, 'base.html', context)
    else:
        form = OpenAPIGeneratorForm()
    return render(request, 'base.html', {'form': form})
