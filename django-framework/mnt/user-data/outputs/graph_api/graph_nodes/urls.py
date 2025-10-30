"""
URL Configuration for graph_nodes app
"""
from django.urls import path
from .views import GetNodesView, GetAllNodesView, GetNodeByIdView

app_name = 'graph_nodes'

urlpatterns = [
    path('nodes/', GetNodesView.as_view(), name='get-nodes'),
    path('nodes/all/', GetAllNodesView.as_view(), name='get-all-nodes'),
    path('nodes/<str:node_id>/', GetNodeByIdView.as_view(), name='get-node-by-id'),
]
