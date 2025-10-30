"""
Main URL Configuration for graph_api project
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Graph Database API",
        default_version='v1',
        description="""
        Graph Database REST API for querying nodes and relationships.
        
        This API provides endpoints to interact with a graph database,
        allowing you to retrieve nodes based on various criteria.
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@graphapi.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('graph_nodes.urls')),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
