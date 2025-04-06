from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import *
from django.db import models
from django.db.models import Q


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client = Client.objects.get(pk=self.kwargs['client_id'])
        project = serializer.save(client=client, created_by=self.request.user)
        project.users.set(self.request.data['users'])

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = Project.objects.get(pk=response.data['id'])
        return Response(ProjectSerializer(instance).data)

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClientCreateSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = Client.objects.get(pk=response.data['id'])
        return Response(ClientSerializer(instance).data)



class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ClientSerializer if self.request.method == 'GET' else ClientCreateSerializer

    def perform_update(self, serializer):
        updated_at = models.DateTimeField(auto_now=True)
        serializer.save(updated_at=updated_at, updated_by=self.request.user)

class UserProjectsListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)



class UserAssignedProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.projects.all()
    

