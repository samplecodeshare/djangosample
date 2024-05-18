# <app_name>/views.py
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
import os

def get_cards(request):
    cards = [
        {"title": "Card 1", "documentation_url": "http://google.com", "description": "Description for Card 1", "tags": ["tag1", "tag2"]},
        {"title": "Card 2", "documentation_url": "http://google.com", "description": "Description for Card 2", "tags": ["tag2", "tag3"]},
        {"title": "Card 3", "documentation_url": "http://google.com",  "description": "Description for Card 3", "tags": ["tag3", "tag4"]},
        {"title": "Card 4", "documentation_url": "http://google.com",  "description": "Description for Card 1", "tags": ["tag1", "tag2"]},
        {"title": "Card 5", "documentation_url": "http://google.com",  "description": "Description for Card 2", "tags": ["tag2", "tag3"]},
        {"title": "Card 6", "documentation_url": "http://google.com",  "description": "Description for Card 3", "tags": ["tag3", "tag4"]},
        {"title": "Card 7", "documentation_url": "http://google.com",  "description": "Description for Card 1", "tags": ["tag1", "tag2"]},
        {"title": "Card 8", "documentation_url": "http://google.com",  "description": "Description for Card 2", "tags": ["tag2", "tag3"]},
        {"title": "Card 9", "documentation_url": "http://google.com",  "description": "Description for Card 3", "tags": ["tag3", "tag4"]},
        {"title": "Card 10", "documentation_url": "http://google.com",  "description": "Description for Card 1", "tags": ["tag1", "tag2"]},
        {"title": "Card 11", "documentation_url": "http://google.com",  "description": "Description for Card 2", "tags": ["tag2", "tag3"]},
        {"title": "Card 12", "documentation_url": "http://google.com",  "description": "Description for Card 3", "tags": ["tag3", "tag4"]},
        # Add more sample cards as needed
    ]
    return JsonResponse(cards, safe=False)

def get_card_params(request):
    card_params = [
        {"full_name": "Alice Cookie", 
         "email": "foobar@example.com", 
         "project_name": "Django Boilerplate",
         "version": "0.1.0",
         "license": ["MIT", "BSD-3", "GNU GPL v3.0", "Apache Software License 2.0"]}
    ]
    return JsonResponse(card_params, safe=False)

@csrf_exempt
def generate_download_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("DATA=" + str(data))
            import time
            time.sleep(10)
            # Process the data here. For example, create a ZIP file based on the data.
            # We'll simulate this by generating a dummy file path.

            # Assuming the ZIP file is created and saved in a directory called 'downloads'
            file_name = 'dummy.zip'
            file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', file_name)

            # Create a download URL
            download_url = request.build_absolute_uri(reverse('download_file', args=[file_name]))

            return JsonResponse({'download_url': download_url}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    else:
        return HttpResponseNotFound('File not found')