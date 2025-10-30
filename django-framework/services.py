"""
Service layer for Graph Database operations
This would typically connect to a real graph database (Neo4j, ArangoDB, etc.)
For demo purposes, we're using dummy data
"""
from datetime import datetime, timezone
from typing import List, Dict, Any


class GraphDatabaseService:
    """
    Service to interact with graph database
    In production, this would connect to actual graph DB
    """
    
    # Dummy graph data
    DUMMY_NODES = [
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
        },
        {
            "node_id": "n002",
            "labels": ["Person", "User"],
            "properties": {
                "name": "Bob Smith",
                "email": "bob@example.com",
                "age": 35,
                "city": "San Francisco",
                "status": "active",
                "join_date": "2022-11-20"
            },
            "created_at": "2022-11-20T09:15:00Z",
            "updated_at": "2024-10-28T11:45:00Z",
            "relationship_count": 8,
            "degree": {
                "incoming": 5,
                "outgoing": 3,
                "total": 8
            }
        },
        {
            "node_id": "n003",
            "labels": ["Person", "Admin"],
            "properties": {
                "name": "Charlie Brown",
                "email": "charlie@example.com",
                "age": 42,
                "city": "Chicago",
                "status": "active",
                "join_date": "2021-03-10"
            },
            "created_at": "2021-03-10T08:00:00Z",
            "updated_at": "2024-10-29T16:30:00Z",
            "relationship_count": 12,
            "degree": {
                "incoming": 7,
                "outgoing": 5,
                "total": 12
            }
        },
        {
            "node_id": "n004",
            "labels": ["Person", "User"],
            "properties": {
                "name": "Diana Prince",
                "email": "diana@example.com",
                "age": 31,
                "city": "Boston",
                "status": "inactive",
                "join_date": "2023-05-22"
            },
            "created_at": "2023-05-22T12:00:00Z",
            "updated_at": "2024-09-15T10:20:00Z",
            "relationship_count": 3,
            "degree": {
                "incoming": 2,
                "outgoing": 1,
                "total": 3
            }
        },
        {
            "node_id": "n005",
            "labels": ["Organization", "Company"],
            "properties": {
                "name": "TechCorp Inc",
                "email": "contact@techcorp.com",
                "city": "Seattle",
                "status": "active",
                "founded": "2015-01-01",
                "employees": 250
            },
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-10-30T08:00:00Z",
            "relationship_count": 15,
            "degree": {
                "incoming": 10,
                "outgoing": 5,
                "total": 15
            }
        },
        {
            "node_id": "n006",
            "labels": ["Person", "User"],
            "properties": {
                "name": "Alice Cooper",
                "email": "alice.cooper@music.com",
                "age": 45,
                "city": "Los Angeles",
                "status": "active",
                "join_date": "2020-08-10"
            },
            "created_at": "2020-08-10T14:20:00Z",
            "updated_at": "2024-10-25T09:10:00Z",
            "relationship_count": 6,
            "degree": {
                "incoming": 4,
                "outgoing": 2,
                "total": 6
            }
        },
    ]
    
    @classmethod
    def get_nodes_by_criteria(cls, by: str, value: str) -> List[Dict[str, Any]]:
        """
        Retrieve nodes based on specified criteria
        
        Args:
            by: Field name to search by
            value: Value to match
            
        Returns:
            List of nodes matching the criteria
        """
        results = []
        
        for node in cls.DUMMY_NODES:
            if by == "node_id":
                if node["node_id"] == value:
                    results.append(node)
            elif by == "label" or by == "type":
                if value in node["labels"]:
                    results.append(node)
            elif by in node["properties"]:
                # Check if property value matches (case-insensitive for strings)
                prop_value = node["properties"][by]
                if isinstance(prop_value, str) and isinstance(value, str):
                    if prop_value.lower() == value.lower():
                        results.append(node)
                elif str(prop_value) == value:
                    results.append(node)
        
        return results
    
    @classmethod
    def get_node_by_id(cls, node_id: str) -> Dict[str, Any]:
        """Get a single node by ID"""
        for node in cls.DUMMY_NODES:
            if node["node_id"] == node_id:
                return node
        return None
    
    @classmethod
    def get_all_nodes(cls) -> List[Dict[str, Any]]:
        """Get all nodes in the graph"""
        return cls.DUMMY_NODES
