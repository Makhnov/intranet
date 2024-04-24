from django.utils.deprecation import MiddlewareMixin
from accompte.models import CGSUserProfile

class CGSProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile = CGSUserProfile.objects.get_or_create(user=request.user)[0]
            request.user_theme = user_profile.theme
            request.user_icons = user_profile.icons
            request.user_avatar_url = user_profile.avatar.url if user_profile.avatar else None
        else:
            request.user_theme = 'default'
            request.user_icons = 'default'
            request.user_avatar_url = None
