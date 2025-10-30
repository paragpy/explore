# Graph Database API - Django REST Framework with Swagger

A Django REST API for querying graph database nodes with Swagger/OpenAPI documentation.

## Project Structure

```
graph_api/
├── manage.py
├── requirements.txt
├── graph_api/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
└── graph_nodes/
    ├── __init__.py
    ├── apps.py
    ├── serializers.py
    ├── services.py
    ├── views.py
    └── urls.py
```

## Features

- **RESTful API** for graph node operations
- **Swagger UI** for interactive API documentation
- **Query nodes** by various criteria (node_id, name, label, properties)
- **Retrieve all nodes** or specific node by ID
- **Dummy data** for demonstration purposes
- **Comprehensive validation** with Django REST Framework serializers

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Start Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### 1. Get Nodes by Criteria
**Endpoint:** `GET /api/nodes/`

**Query Parameters:**
- `by`: Field to query by (node_id, name, label, type, email, age, city, status)
- `value`: Value to search for

**Examples:**
```bash
# Get node by ID
GET /api/nodes/?by=node_id&value=n001

# Get nodes by name
GET /api/nodes/?by=name&value=Alice Johnson

# Get nodes by label
GET /api/nodes/?by=label&value=Person

# Get nodes by city
GET /api/nodes/?by=city&value=New York

# Get nodes by status
GET /api/nodes/?by=status&value=active
```

### 2. Get All Nodes
**Endpoint:** `GET /api/nodes/all/`

**Example:**
```bash
GET /api/nodes/all/
```

### 3. Get Node by ID
**Endpoint:** `GET /api/nodes/{node_id}/`

**Example:**
```bash
GET /api/nodes/n001/
```

## Swagger Documentation

Access the interactive API documentation at:

- **Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/
- **JSON Schema:** http://127.0.0.1:8000/swagger.json

## Sample Response

### Query by Name
**Request:**
```
GET /api/nodes/?by=name&value=Alice Johnson
```

**Response:**
```json
{
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
```

### Query by Label
**Request:**
```
GET /api/nodes/?by=label&value=Person
```

**Response:**
```json
{
  "count": 5,
  "query_params": {
    "by": "label",
    "value": "Person"
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
    }
  ]
}
```

### Get All Nodes
**Request:**
```
GET /api/nodes/all/
```

**Response:**
```json
{
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
    // ... more nodes
  ]
}
```

## Dummy Data

The API includes 6 dummy nodes:

1. **n001** - Alice Johnson (Person, User) - New York
2. **n002** - Bob Smith (Person, User) - San Francisco
3. **n003** - Charlie Brown (Person, Admin) - Chicago
4. **n004** - Diana Prince (Person, User) - Boston
5. **n005** - TechCorp Inc (Organization, Company) - Seattle
6. **n006** - Alice Cooper (Person, User) - Los Angeles

## Supported Query Fields

- `node_id`: Unique node identifier
- `name`: Node name property
- `label` or `type`: Node label/type
- `email`: Email property
- `age`: Age property
- `city`: City property
- `status`: Status property (active/inactive)

## Architecture

### Layers

1. **Views Layer** (`views.py`): Handles HTTP requests and responses
2. **Serializers Layer** (`serializers.py`): Data validation and serialization
3. **Service Layer** (`services.py`): Business logic and data access
4. **URL Configuration** (`urls.py`): Route mapping

### Design Patterns

- **Service Layer Pattern**: Business logic separated from views
- **Serializer Pattern**: Data validation and transformation
- **RESTful API Design**: Standard HTTP methods and status codes

## Extending the API

### Connect to Real Graph Database

Replace the dummy data in `services.py` with actual database connections:

```python
from neo4j import GraphDatabase  # or your preferred graph DB

class GraphDatabaseService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password")
        )
    
    def get_nodes_by_criteria(self, by, value):
        with self.driver.session() as session:
            query = f"MATCH (n) WHERE n.{by} = $value RETURN n"
            result = session.run(query, value=value)
            return [record["n"] for record in result]
```

### Add More Query Operations

Extend the API with additional endpoints for:
- Relationship queries
- Path finding
- Graph traversals
- Aggregations

## Testing with cURL

```bash
# Get node by ID
curl "http://127.0.0.1:8000/api/nodes/?by=node_id&value=n001"

# Get nodes by city
curl "http://127.0.0.1:8000/api/nodes/?by=city&value=New%20York"

# Get all nodes
curl "http://127.0.0.1:8000/api/nodes/all/"

# Get specific node
curl "http://127.0.0.1:8000/api/nodes/n001/"
```

## Testing with Python requests

```python
import requests

# Get nodes by name
response = requests.get(
    "http://127.0.0.1:8000/api/nodes/",
    params={"by": "name", "value": "Alice Johnson"}
)
print(response.json())

# Get all nodes
response = requests.get("http://127.0.0.1:8000/api/nodes/all/")
print(response.json())
```

## License

MIT License
