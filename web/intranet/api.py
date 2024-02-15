from wagtail.api.v2.views import PagesAPIViewSet, BaseAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from wagtailmedia.api.views import MediaAPIViewSet
from django.contrib.auth.models import Group
from users.models import User
from administration.models import ConvocationUser

from .serializers import (
    GroupSerializer,
    CustomPageSerializer,
    UserSerializer,
    ConvocationUserSerializer,
)

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

    
class UserGroupsAPIViewSet(BaseAPIViewSet):
    base_serializer_class = GroupSerializer
    model = Group
    name = "user_groups"
    paginate_by = None

    def get_queryset(self):
        user = self.request.user
        return user.groups.all()

class CustomPagesAPIViewSet(PagesAPIViewSet):
    base_serializer_class = CustomPageSerializer
    paginate_by = None
        
class UsersAPIViewSet(BaseAPIViewSet):
    base_serializer_class = UserSerializer
    model = User
    name = "users"
    paginate_by = None

    def get_queryset(self):
        return User.objects.all()
    
class ConvocationUsersAPIViewSet(BaseAPIViewSet):
    base_serializer_class = ConvocationUserSerializer
    model = ConvocationUser
    name = "convocation_users"
    paginate_by = None

    def get_queryset(self):
        return ConvocationUser.objects.all()
    
class GroupsAPIViewSet(BaseAPIViewSet):
    base_serializer_class = ConvocationUserSerializer
    model = ConvocationUser
    name = "convocation_users"
    paginate_by = None

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint("pages", CustomPagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("media", MediaAPIViewSet)
api_router.register_endpoint("users", UsersAPIViewSet)
api_router.register_endpoint("user_groups", UserGroupsAPIViewSet)
api_router.register_endpoint("convocation_users", ConvocationUsersAPIViewSet)
