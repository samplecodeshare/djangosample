import requests
from django.shortcuts import render
from django import forms

class DynamicForm(forms.Form):
    pass  # Dynamic form fields will be added programmatically
