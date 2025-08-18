from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import mimetypes


def serve_media(request, file_path):
    """
    Serve media files in production
    """
    # Security: only allow files in the media directory
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Normalize path to prevent directory traversal attacks
    full_path = os.path.normpath(full_path)
    
    # Ensure the file is within MEDIA_ROOT
    if not full_path.startswith(settings.MEDIA_ROOT):
        raise Http404("File not found")
    
    # Check if file exists
    if not os.path.exists(full_path):
        raise Http404("File not found")
    
    # Guess content type
    content_type, _ = mimetypes.guess_type(full_path)
    
    # Return file response
    try:
        response = FileResponse(
            open(full_path, 'rb'),
            content_type=content_type or 'application/octet-stream'
        )
        return response
    except IOError:
        raise Http404("File not found")
