"""
Serializers for Graph Node API
"""
from rest_framework import serializers


class NodeQuerySerializer(serializers.Serializer):
    """
    Serializer for querying nodes by various criteria
    """
    by = serializers.CharField(
        required=True,
        help_text="Field to query by (e.g., 'node_id', 'name', 'label', 'property_name')"
    )
    value = serializers.CharField(
        required=True,
        help_text="Value to search for"
    )

    def validate_by(self, value):
        """
        Validate that 'by' parameter is one of the allowed fields
        """
        allowed_fields = ['node_id', 'name', 'label', 'type', 'email', 'age', 'city', 'status']
        if value not in allowed_fields:
            raise serializers.ValidationError(
                f"Invalid field '{value}'. Allowed fields are: {', '.join(allowed_fields)}"
            )
        return value


class NodePropertySerializer(serializers.Serializer):
    """
    Serializer for node properties
    """
    key = serializers.CharField()
    value = serializers.JSONField()
    data_type = serializers.CharField()


class NodeRelationshipSerializer(serializers.Serializer):
    """
    Serializer for node relationships
    """
    relationship_id = serializers.CharField()
    type = serializers.CharField()
    direction = serializers.ChoiceField(choices=['OUTGOING', 'INCOMING', 'BIDIRECTIONAL'])
    target_node_id = serializers.CharField()
    properties = serializers.DictField(required=False)


class NodeDetailSerializer(serializers.Serializer):
    """
    Serializer for complete node details
    """
    node_id = serializers.CharField(help_text="Unique identifier for the node")
    labels = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of labels/types assigned to this node"
    )
    properties = serializers.DictField(
        help_text="All properties of the node as key-value pairs"
    )
    created_at = serializers.DateTimeField(help_text="Node creation timestamp")
    updated_at = serializers.DateTimeField(help_text="Last update timestamp")
    relationship_count = serializers.IntegerField(
        help_text="Total number of relationships connected to this node"
    )
    degree = serializers.DictField(
        help_text="Degree information (incoming, outgoing, total)"
    )


class NodeListResponseSerializer(serializers.Serializer):
    """
    Serializer for response containing list of nodes
    """
    count = serializers.IntegerField(help_text="Total number of nodes found")
    query_params = serializers.DictField(help_text="Parameters used for the query")
    nodes = NodeDetailSerializer(many=True, help_text="List of nodes matching the query")
