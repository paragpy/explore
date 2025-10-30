# Quick Reference Guide - Graph Database API

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Start server
python manage.py runserver

# Or use the quick start script
chmod +x start.sh
./start.sh
```

## 📍 Important URLs

- **API Base**: http://127.0.0.1:8000/api/
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin**: http://127.0.0.1:8000/admin/

## 🎯 Available Endpoints

### 1. Get Nodes by Criteria
```
GET /api/nodes/?by={field}&value={value}
```

**Supported fields:**
- `node_id` - Unique identifier
- `name` - Node name
- `label` or `type` - Node label/type
- `email` - Email address
- `age` - Age value
- `city` - City name
- `status` - Status (active/inactive)

**Examples:**
```bash
# By ID
curl "http://127.0.0.1:8000/api/nodes/?by=node_id&value=n001"

# By name
curl "http://127.0.0.1:8000/api/nodes/?by=name&value=Alice%20Johnson"

# By label
curl "http://127.0.0.1:8000/api/nodes/?by=label&value=Person"

# By city
curl "http://127.0.0.1:8000/api/nodes/?by=city&value=New%20York"

# By status
curl "http://127.0.0.1:8000/api/nodes/?by=status&value=active"
```

### 2. Get All Nodes
```
GET /api/nodes/all/
```

**Example:**
```bash
curl "http://127.0.0.1:8000/api/nodes/all/"
```

### 3. Get Node by ID
```
GET /api/nodes/{node_id}/
```

**Example:**
```bash
curl "http://127.0.0.1:8000/api/nodes/n001/"
```

## 📊 Sample Data

The API includes 6 dummy nodes:

| Node ID | Name | Labels | City | Status |
|---------|------|--------|------|--------|
| n001 | Alice Johnson | Person, User | New York | active |
| n002 | Bob Smith | Person, User | San Francisco | active |
| n003 | Charlie Brown | Person, Admin | Chicago | active |
| n004 | Diana Prince | Person, User | Boston | inactive |
| n005 | TechCorp Inc | Organization, Company | Seattle | active |
| n006 | Alice Cooper | Person, User | Los Angeles | active |

## 📝 Response Format

### Successful Query
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

### No Results Found (404)
```json
{
  "count": 0,
  "query_params": {
    "by": "name",
    "value": "NonExistent"
  },
  "nodes": [],
  "message": "No nodes found matching the specified criteria"
}
```

### Invalid Request (400)
```json
{
  "error": {
    "by": [
      "Invalid field 'invalid_field'. Allowed fields are: node_id, name, label, type, email, age, city, status"
    ]
  }
}
```

## 🏗️ Project Structure

```
graph_api/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── start.sh                     # Quick start script
├── README.md                    # Main documentation
├── EXAMPLES.md                  # API examples
├── ARCHITECTURE.md              # Architecture details
│
├── graph_api/                   # Main project folder
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   └── urls.py                  # URL configuration with Swagger
│
└── graph_nodes/                 # Graph nodes app
    ├── __init__.py
    ├── apps.py                  # App configuration
    ├── serializers.py           # Data validation & serialization
    ├── services.py              # Business logic & data access
    ├── views.py                 # API endpoints
    └── urls.py                  # App URL routing
```

## 🔧 Key Components

### Serializers (`serializers.py`)
- `NodeQuerySerializer` - Validates query parameters
- `NodeDetailSerializer` - Node data structure
- `NodeListResponseSerializer` - Response format

### Services (`services.py`)
- `GraphDatabaseService` - Business logic layer
  - `get_nodes_by_criteria()` - Query nodes
  - `get_node_by_id()` - Get single node
  - `get_all_nodes()` - Get all nodes

### Views (`views.py`)
- `GetNodesView` - Query nodes by criteria
- `GetAllNodesView` - Retrieve all nodes
- `GetNodeByIdView` - Get specific node

## 🧪 Testing with Python

```python
import requests

base_url = "http://127.0.0.1:8000/api"

# Get nodes by city
response = requests.get(
    f"{base_url}/nodes/",
    params={"by": "city", "value": "New York"}
)
print(response.json())

# Get all nodes
response = requests.get(f"{base_url}/nodes/all/")
print(response.json())

# Get specific node
response = requests.get(f"{base_url}/nodes/n001/")
print(response.json())
```

## 🔌 Connecting Real Graph Database

To connect to a real graph database (e.g., Neo4j):

1. Install driver:
```bash
pip install neo4j
```

2. Update `services.py`:
```python
from neo4j import GraphDatabase

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
            # Transform results...
```

## 📚 Documentation Files

- **README.md** - Main documentation and setup guide
- **EXAMPLES.md** - Detailed API examples with responses
- **ARCHITECTURE.md** - System architecture and design patterns
- **QUICK_REFERENCE.md** - This file (quick reference)

## 💡 Tips

1. **Try Swagger UI** - Best way to explore the API interactively
2. **Check Response Status** - 200 (success), 404 (not found), 400 (bad request)
3. **URL Encode Values** - Use %20 for spaces in query parameters
4. **Case Sensitivity** - String comparisons are case-insensitive
5. **Multiple Results** - Query by label/city can return multiple nodes

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
python manage.py runserver 8001
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Cannot access from other machines
```bash
# Allow external access
python manage.py runserver 0.0.0.0:8000
```

## 📞 HTTP Status Codes

- **200 OK** - Request successful
- **400 Bad Request** - Invalid parameters
- **404 Not Found** - No nodes found
- **500 Internal Server Error** - Server error

## 🎓 Next Steps

1. Explore the Swagger UI
2. Try different query combinations
3. Review the architecture documentation
4. Connect to a real graph database
5. Add authentication
6. Implement more endpoints (relationships, paths, etc.)
