from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse, Http404

def file_view(request, filename):
    # Make sure the requested file exists in the 'files' directory
    file_path = os.path.join(settings.BASE_DIR, 'files', filename)
    if not os.path.exists(file_path):
        raise Http404

    # Open the file and return its contents as a response
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
