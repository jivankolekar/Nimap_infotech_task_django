from django.urls import path
from .views import *

urlpatterns = [
    path('', ClientListCreateView.as_view()),
    path('clients/', ClientListCreateView.as_view()),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view()),
    path('projects/', UserProjectsListView.as_view(), name='user-projects'),
    path('clients/<int:client_id>/projects/', ProjectCreateView.as_view(), name='create-project'),
]
