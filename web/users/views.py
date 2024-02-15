from django.shortcuts import render
from .serializers import CustomUserDetailsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserDetailsSerializer
from wagtail.users.views.users import Index as OriginalIndexView
from django.utils.translation import gettext_lazy as _

def profile_view(request):
    return render(request, "account/profile.html")


class UserPermissionDetailsView(APIView):
    def get(self, request):
        serializer = CustomUserDetailsSerializer(request.user)
        return Response(serializer.data)


class CustomUserIndexView(OriginalIndexView):
        
    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', '20')
        if paginate_by.isdigit():
            return int(paginate_by)
        return 20  # Defaut


    def get_valid_orderings(self):
        return super().get_valid_orderings() + [
            "name",
            "-name",
            "level",
            "-level",
            "municipality",
            "-municipality",
            "status",
            "-status",
        ]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Tri par nom
        if self.get_ordering() == "name":
            queryset = queryset.order_by("first_name", "last_name")

        if self.get_ordering() == "-name":
            queryset = queryset.order_by("-first_name", "-last_name")
        
        # Tri par niveau d'accès
        if self.get_ordering() == "level":
            queryset = queryset.order_by("-is_superuser", "-is_staff")
            
        if self.get_ordering() == "-level":
            queryset = queryset.order_by("is_superuser", "is_staff")                
            
        # Tri par communes
        if self.get_ordering() == "municipality":
            queryset = queryset.order_by("municipality")
            
        if self.get_ordering() == "-municipality":
            queryset = queryset.order_by("-municipality")
                
        # Tri par statut 
        if self.get_ordering() == "status":
            queryset = queryset.order_by("-is_active")
            
        if self.get_ordering() == "-status":
            queryset = queryset.order_by("is_active")
            
        # Tri par groupes
        if self.get_ordering() == "groups":
            queryset = queryset.order_by('groups')
            
        if self.get_ordering() == "-groups":
            queryset = queryset.order_by('-groups')

        return queryset