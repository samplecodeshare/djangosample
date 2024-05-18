from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import requests
from django.shortcuts import render
from django import forms
from django.views.decorators.cache import cache_page
from loguru import logger
from django.conf import settings
import os

class DynamicForm(forms.Form):
    pass  # Dynamic form fields will be added programmatically


def hello_world(request):
    return HttpResponse("Hello, World!")

def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if a_set.intersection(b_set): 
        return True 
    else: 
        return False 

# @cache_page(60 * 15)  # Cache this view for 15 minutes
def card_list(request):
    # URL of the REST API endpoint that returns the list of cards
    api_url = 'http://localhost:8000/api/cards/'

    selected_tags = request.GET.getlist('tags')
    logger.debug("Selected Tags.." + str(selected_tags))

    try:
        # Make a GET request to the API endpoint
        response = requests.get(api_url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response into a Python list of cards
            cards = response.json()

            # Initialize an empty set to store unique tags
            unique_tags = set()
            selected_cards = []

            # Loop through each card
            for card in cards:
                # Split the tags string into individual tags
                tags = card['tags']
                if selected_tags :
                    if common_member(tags,selected_tags):
                        selected_cards.append(card)
                else:
                    selected_cards.append(card)
                
                # Add each tag to the set of unique tags
                unique_tags.update(tags)

            # Convert the set to a sorted list (optional)
            sorted_unique_tags = sorted(unique_tags)
            logger.debug("Selected Tags = " + str(selected_tags) + "Tags =" + str(tags))

            # Pass the list of cards to the template for rendering
            return render(request, 'card_list.html', {'cards': selected_cards, 'tags': sorted(sorted_unique_tags),'selected_tags': selected_tags})
        else:
            # If the request was not successful, raise an exception
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        error_message = f'Error fetching cards from API: {str(e)}'
        return render(request, 'error.html', {'error_message': error_message})

def get_parameters_from_api(card_name):
    # Call the REST API to get parameters based on the card name
    api_url = f"http://localhost:8000/api/cardparams/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def card_form(request):
    if request.method == 'POST':
        # Process form submission if needed
        pass
    else:
        card_name = request.GET.get('card_name')
        parameters = get_parameters_from_api(card_name)
        print("parameters==" + str(parameters))
        if parameters[0]:
            # Dynamically generate a form based on parameters
            dynamic_fields = {}
            for key, value in parameters[0].items():
                # dynamic_fields[key] = forms.CharField(initial=value, label=key.replace('_', ' ').title())

                logger.info("Type of the value in cookiecutterjson is = " + str(type(value)))
                if (isinstance(value, list)):
                    choices = [(option, option) for option in value]
                    dynamic_fields[key] = forms.ChoiceField(
                        label=key.replace('_', ' ').title(),
                        choices=choices,  # Choices will be populated in the view
                        widget=forms.Select(attrs={'class': 'form-control'})
                    )
                else:                    
                    dynamic_fields[key] = forms.CharField(
                        label=key.replace('_', ' ').title(),
                        min_length=0,  # Minimum number of characters
                        max_length=50,  # Maximum number of characters
                        initial= value,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': value})
                    )

            DynamicForm.base_fields.update(dynamic_fields)
            form = DynamicForm()
        else:
            form = None

    return render(request, 'card_form.html', {'form': form , 'card_name':card_name })

def log_view(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'debug.log' )
    logger.info("Log file =" + log_file_path)
    
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            log_content = file.read()
    else:
        log_content = "Log file not found."
    
    return render(request, 'log_template.html', {'log_content': log_content})