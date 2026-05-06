from django.shortcuts import render

import logging
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

# Initialize the logger configured in settings.py
logger = logging.getLogger(__name__)

# Apply rate limiting: Max 5 requests per minute per IP. Block if exceeded.
@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)
def secure_login_view(request):
    if request.method == 'POST':
        # Simulated authentication logic
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Simulated failure for testing purposes
        if username != "admin" or password != "securepass":
            # Part D: Secure Logging
            logger.warning(f"Failed login attempt detected from IP: {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({"error": "Invalid credentials"}, status=401)
            
        return JsonResponse({"message": "Login successful!"})
        
    return JsonResponse({"error": "POST method required"}, status=405)