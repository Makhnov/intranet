from rest_framework import serializers
from wagtail.models import PageViewRestriction, Page
from django.contrib.auth.models import Permission, Group
from wagtail.api.v2.serializers import PageSerializer, get_serializer_class
from wagtail.api.v2.utils import get_object_detail_url
from django.contrib.auth import get_user_model
from administration.models import ConvocationUser, ConvocationPage, CompteRenduPage

# from wagtail_maps.api.serializers import MapSerializer
# from wagtail_maps.models import Map
from rest_framework import relations
from wagtailmedia.models import get_media_model
from wagtail.api.v2.utils import get_full_url
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.StringRelatedField()

    class Meta:
        model = Permission
        fields = ["name", "codename", "content_type"]


class GroupSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "type", "detail_url"]

    def get_type(self, obj):
        return f"{obj._meta.app_label}.{obj._meta.model_name}"

    def get_detail_url(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "wagtailapi_router"):
            return get_object_detail_url(
                request.wagtailapi_router, request, Group, obj.pk
            )
        return ""

    def get_permissions(self, obj):
        return [permission.codename for permission in obj.permissions.all()]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["name"] = instance.name

        # Serialise the permissions
        permission_serializer = PermissionSerializer(
            instance.permissions.all(), many=True
        )
        rep["permissions"] = permission_serializer.data

        return rep

    
class CustomPageParentField(relations.RelatedField):
    logo = serializers.SerializerMethodField()
    
    def get_attribute(self, instance):
        parent = instance.get_parent()

        if self.context["base_queryset"].filter(id=parent.id).exists():
            return parent
             
    def to_representation(self, value):
        # Récupérez la version spécifique de la page
        specific_value = value.specific

        serializer_class = get_serializer_class(
            specific_value.__class__,
            ["id", "type", "detail_url", "html_url", "title"],
            meta_fields=["type", "detail_url", "html_url"],
            base=PageSerializer,
        )
        serializer = serializer_class(context=self.context)
        representation = serializer.to_representation(specific_value)

        # Maintenant, vous pouvez accéder aux champs spécifiques à la sous-classe
        if hasattr(specific_value, 'logo') and specific_value.logo:
            representation['meta']['logo'] = {
                'id': specific_value.logo.id,
                'url': specific_value.logo.file.url,
                'title': specific_value.logo.title
            }

        if hasattr(specific_value, 'tooltip') and specific_value.tooltip:
            representation['meta']['tooltip'] = specific_value.tooltip

        return representation

    
class CustomPageSerializer(PageSerializer):   
    parent = CustomPageParentField(read_only=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meta']['date'] = getattr(instance, 'date', None)        
        data['compte_rendu_page'] = self.get_compte_rendu_page(instance)        
        data["convocation_users"] = self.get_convocation_users(instance)
        data['old'] = getattr(instance, 'old', None)
        
        media_id = getattr(instance, 'media_id', None)        
        if media_id:
            data["media_details"] = self.get_media_details(media_id)
        else:
            data["media_details"] = None        
            
        data["view_restrictions"] = self.get_view_restrictions(instance)
        
        return data
    
    def get_media_details(self, media_id):
        try:
            media = get_media_model().objects.get(id=media_id)
        except get_media_model().DoesNotExist:
            return None

        data = {
            "title": media.title,
            "width": media.width,
            "height": media.height,
            "media_type": media.type,
            "collection": {
                "id": media.collection.id,
                "title": media.collection.name
            },
            "tags": list(media.tags.names()),
            "download_url": get_full_url(self.context["request"], media.url)
        }        
        return data

    def get_view_restrictions(self, obj):
        restrictions = PageViewRestriction.objects.filter(page_id=obj.id).values(
            "id", "password", "restriction_type"
        )

        # Enrich each restriction with the associated groups
        for restriction in restrictions:
            restriction_id = restriction["id"]
            restriction_instance = PageViewRestriction.objects.get(id=restriction_id)
            groups = restriction_instance.groups.all().values_list("id", flat=True)
            restriction["groups"] = list(groups)

        return list(restrictions)

    def get_convocation_users(self, obj):
        if not isinstance(obj, ConvocationPage):
            return None        
        try:            
            queryset = ConvocationUser.objects.filter(convocation__page_ptr=obj).order_by('user__last_name', 'user__first_name')
            serializer = SimplifiedConvocationUserSerializer(instance=queryset, many=True, context=self.context)
            return serializer.data
        except ConvocationUser.DoesNotExist:
            return None

    def get_compte_rendu_page(self, obj):
        if not isinstance(obj, ConvocationPage):
            return None        
        try:
            compte_rendu_page = CompteRenduPage.objects.get(convocation=obj)
            serializer = SimplifiedCompteRenduSerializer(compte_rendu_page, context=self.context)
            return serializer.data
        except CompteRenduPage.DoesNotExist:
            return None
        
    
class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return f"{obj._meta.app_label}.{obj._meta.model_name}"

    def get_detail_url(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "wagtailapi_router"):
            return get_object_detail_url(
                request.wagtailapi_router, request, get_user_model(), obj.pk
            )
        return ""
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('type', None)        
        data['name'] = instance.last_name.upper() + ' ' + instance.first_name
        data['elected'] = instance.function_council
        return data
    
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "detail_url",
            "type",
            "first_name",
            "last_name",
            "civility",
            "date_of_birth",
            "address1",
            "address2",
            "zip_code",
            "city",
            "mobile_phone",
            "municipality",
            "function_municipality",
            "function_council",
            "commissions",
            "functions_commissions",
            "function_bureau",
            "function_conference",
            "username",
            "email",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]


class ConvocationUserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    parent_url = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return f"{obj._meta.app_label}.{obj._meta.model_name}"

    def get_detail_url(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "wagtailapi_router"):
            return get_object_detail_url(
                request.wagtailapi_router, request, ConvocationUser, obj.pk
            )
        return ""
    
    def get_parent_url(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "wagtailapi_router"):
            return get_object_detail_url(
                request.wagtailapi_router, request, Page, obj.parent.id
            )
        return None
    
    def get_convocation_url(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "wagtailapi_router"):
            return get_object_detail_url(
                request.wagtailapi_router, request, ConvocationPage, obj.convocation.id
            )
        return None

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('id', None)
        data.pop('type', None)        
        data['Convocation'] = instance.convocation.title
        data['Convocation_url'] = self.get_convocation_url(instance)
        request = self.context.get('request', None)
        if request is not None:
            data['Convocation_html'] = request.build_absolute_uri(instance.convocation.url)
        else:
            data['Convocation_html'] = instance.convocation.url 
                
        return data

    class Meta:
        model = ConvocationUser
        fields = [
            'id',
            'type',
            'detail_url',
            'user',
            'parent',
            'parent_url',
            'function',
            'function_weight',
            'gender',
            'identity',
            'municipality',
            'presence',
            'substitute',
            'alternate',
            'Convocation_url',
            'Convocation_html',
        ]


class SimplifiedConvocationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocationUser
        fields = [
            'id',
            'user',
            'function',
            'function_weight',
            'gender',
            'identity',
            'municipality',
            'presence',
            'substitute',
            'alternate',
        ]
        

class SimplifiedCompteRenduSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteRenduPage
        fields = [
            'id',
            'title',
            'convocation',
            'secretary',
            'substitute_users',
            'replaced_users',
            'unreplaced_users',  
            'date',
            'quorum',
            'body',
        ]