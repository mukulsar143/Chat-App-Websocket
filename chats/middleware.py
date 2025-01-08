from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class RoleBasedAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            request.role = user_profile.role if user_profile else None
# middleware.py
from django.http import HttpResponse
import re

class DeviceDetectionMiddleware:
    MOBILE_USER_AGENTS = [
        "Mobile", "iPhone", "Android", "Windows Phone", "BlackBerry", "IEMobile"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the User-Agent contains mobile-specific keywords
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        is_mobile = any(mobile_user_agent in user_agent for mobile_user_agent in self.MOBILE_USER_AGENTS)

        # Attach the result to the request object
        request.is_mobile = is_mobile
        
        response = self.get_response(request)
        return response
