from django.contrib.auth.models import Permission, Group
from dj_rest_auth.serializers import (
    UserDetailsSerializer as DefaultUserDetailsSerializer,
)
from rest_framework import serializers
from wagtail.api.v2.utils import get_object_detail_url


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


class CustomUserDetailsSerializer(DefaultUserDetailsSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta(DefaultUserDetailsSerializer.Meta):
        fields = DefaultUserDetailsSerializer.Meta.fields + (
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
        )
