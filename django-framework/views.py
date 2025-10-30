"""
Views for Graph Node API
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    NodeQuerySerializer,
    NodeDetailSerializer,
    NodeListResponseSerializer
)
from .services import GraphDatabaseService


class GetNodesView(APIView):
    """
    API endpoint to retrieve nodes from the graph database based on criteria.
    
    This endpoint accepts multiple query parameters to filter nodes by various fields
    such as node_id, name, label, or any custom property.
    """
    
    @swagger_auto_schema(
        operation_description="""
        Retrieve nodes from the graph database based on specified criteria.
        
        **Query Parameters:**
        - `by`: The field to query by (e.g., 'node_id', 'name', 'label', 'email', 'city', 'status', 'age')
        - `value`: The value to search for in the specified field
        
        **Examples:**
        - Get node by ID: `?by=node_id&value=n001`
        - Get nodes by name: `?by=name&value=Alice Johnson`
        - Get nodes by label: `?by=label&value=Person`
        - Get nodes by city: `?by=city&value=New York`
        - Get nodes by status: `?by=status&value=active`
        
        **Supported 'by' fields:**
        - `node_id`: Unique node identifier
        - `name`: Node name property
        - `label` or `type`: Node label/type
        - `email`: Email property
        - `age`: Age property
        - `city`: City property
        - `status`: Status property
        """,
        manual_parameters=[
            openapi.Parameter(
                'by',
                openapi.IN_QUERY,
                description="Field to query by (node_id, name, label, type, email, age, city, status)",
                type=openapi.TYPE_STRING,
                required=True,
                enum=['node_id', 'name', 'label', 'type', 'email', 'age', 'city', 'status']
            ),
            openapi.Parameter(
                'value',
                openapi.IN_QUERY,
                description="Value to search for",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful retrieval of nodes",
                schema=NodeListResponseSerializer(),
                examples={
                    "application/json": {
                        "count": 1,
                        "query_params": {
                            "by": "name",
                            "value": "Alice Johnson"
                        },
                        "nodes": [
                            {
                                "node_id": "n001",
                                "labels": ["Person", "User"],
                                "properties": {
                                    "name": "Alice Johnson",
                                    "email": "alice@example.com",
                                    "age": 28,
                                    "city": "New York",
                                    "status": "active",
                                    "join_date": "2023-01-15"
                                },
                                "created_at": "2023-01-15T10:30:00Z",
                                "updated_at": "2024-10-20T14:22:00Z",
                                "relationship_count": 5,
                                "degree": {
                                    "incoming": 3,
                                    "outgoing": 2,
                                    "total": 5
                                }
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request - Invalid parameters",
                examples={
                    "application/json": {
                        "error": "Invalid field 'invalid_field'. Allowed fields are: node_id, name, label, type, email, age, city, status"
                    }
                }
            ),
            404: openapi.Response(
                description="No nodes found matching the criteria",
                examples={
                    "application/json": {
                        "count": 0,
                        "query_params": {
                            "by": "name",
                            "value": "NonExistent"
                        },
                        "nodes": [],
                        "message": "No nodes found matching the specified criteria"
                    }
                }
            )
        },
        tags=['Graph Nodes']
    )
    def get(self, request):
        """
        Handle GET request to retrieve nodes
        """
        # Validate query parameters
        serializer = NodeQuerySerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract validated data
        by = serializer.validated_data['by']
        value = serializer.validated_data['value']
        
        # Query the graph database
        nodes = GraphDatabaseService.get_nodes_by_criteria(by, value)
        
        # Prepare response
        response_data = {
            "count": len(nodes),
            "query_params": {
                "by": by,
                "value": value
            },
            "nodes": nodes
        }
        
        # Add message if no nodes found
        if len(nodes) == 0:
            response_data["message"] = "No nodes found matching the specified criteria"
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        return Response(response_data, status=status.HTTP_200_OK)


class GetAllNodesView(APIView):
    """
    API endpoint to retrieve all nodes from the graph database.
    """
    
    @swagger_auto_schema(
        operation_description="""
        Retrieve all nodes from the graph database.
        
        This endpoint returns all nodes without any filtering.
        Useful for getting a complete view of the graph structure.
        """,
        responses={
            200: openapi.Response(
                description="Successful retrieval of all nodes",
                schema=NodeListResponseSerializer(),
                examples={
                    "application/json": {
                        "count": 6,
                        "nodes": [
                            {
                                "node_id": "n001",
                                "labels": ["Person", "User"],
                                "properties": {
                                    "name": "Alice Johnson",
                                    "email": "alice@example.com",
                                    "age": 28,
                                    "city": "New York",
                                    "status": "active"
                                },
                                "created_at": "2023-01-15T10:30:00Z",
                                "updated_at": "2024-10-20T14:22:00Z",
                                "relationship_count": 5,
                                "degree": {
                                    "incoming": 3,
                                    "outgoing": 2,
                                    "total": 5
                                }
                            }
                        ]
                    }
                }
            )
        },
        tags=['Graph Nodes']
    )
    def get(self, request):
        """
        Handle GET request to retrieve all nodes
        """
        nodes = GraphDatabaseService.get_all_nodes()
        
        response_data = {
            "count": len(nodes),
            "nodes": nodes
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class GetNodeByIdView(APIView):
    """
    API endpoint to retrieve a specific node by its ID.
    """
    
    @swagger_auto_schema(
        operation_description="""
        Retrieve a specific node by its unique identifier.
        
        **Path Parameter:**
        - `node_id`: The unique identifier of the node
        
        **Example:**
        - `/api/nodes/n001/`
        """,
        responses={
            200: openapi.Response(
                description="Node found successfully",
                schema=NodeDetailSerializer(),
                examples={
                    "application/json": {
                        "node_id": "n001",
                        "labels": ["Person", "User"],
                        "properties": {
                            "name": "Alice Johnson",
                            "email": "alice@example.com",
                            "age": 28,
                            "city": "New York",
                            "status": "active",
                            "join_date": "2023-01-15"
                        },
                        "created_at": "2023-01-15T10:30:00Z",
                        "updated_at": "2024-10-20T14:22:00Z",
                        "relationship_count": 5,
                        "degree": {
                            "incoming": 3,
                            "outgoing": 2,
                            "total": 5
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Node not found",
                examples={
                    "application/json": {
                        "error": "Node with ID 'n999' not found"
                    }
                }
            )
        },
        tags=['Graph Nodes']
    )
    def get(self, request, node_id):
        """
        Handle GET request to retrieve a specific node by ID
        """
        node = GraphDatabaseService.get_node_by_id(node_id)
        
        if node is None:
            return Response(
                {"error": f"Node with ID '{node_id}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(node, status=status.HTTP_200_OK)
