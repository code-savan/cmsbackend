from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import requests
from django.conf import settings
from .models import Contract
from .serializers import ContractSerializer
from rest_framework.permissions import IsAuthenticated

class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Contract model.
    Includes custom actions for file upload and contract management.
    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get_queryset(self):
        """Return contracts for the current authenticated user only"""
        return Contract.objects.filter(user=self.request.user)
