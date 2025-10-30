# Example API Requests

## Using cURL

### 1. Get Node by ID
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=node_id&value=n001" -H "accept: application/json"
```

**Expected Response:**
```json
{
  "count": 1,
  "query_params": {
    "by": "node_id",
    "value": "n001"
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

### 2. Get Nodes by Name
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=name&value=Bob%20Smith" -H "accept: application/json"
```

**Expected Response:**
```json
{
  "count": 1,
  "query_params": {
    "by": "name",
    "value": "Bob Smith"
  },
  "nodes": [
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

### 3. Get Nodes by Label
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=label&value=Person" -H "accept: application/json"
```

**Expected Response:**
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

### 4. Get Nodes by City
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=city&value=Chicago" -H "accept: application/json"
```

**Expected Response:**
```json
{
  "count": 1,
  "query_params": {
    "by": "city",
    "value": "Chicago"
  },
  "nodes": [
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
    }
  ]
}
```

### 5. Get Nodes by Status
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=status&value=active" -H "accept: application/json"
```

**Expected Response:**
```json
{
  "count": 5,
  "query_params": {
    "by": "status",
    "value": "active"
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

### 6. Get All Nodes
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/all/" -H "accept: application/json"
```

**Expected Response:**
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
    }
  ]
}
```

### 7. Get Specific Node by ID (Direct URL)
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/n001/" -H "accept: application/json"
```

**Expected Response:**
```json
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
```

### 8. Error Case - Invalid Field
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=invalid_field&value=test" -H "accept: application/json"
```

**Expected Response (400 Bad Request):**
```json
{
  "error": {
    "by": [
      "Invalid field 'invalid_field'. Allowed fields are: node_id, name, label, type, email, age, city, status"
    ]
  }
}
```

### 9. Error Case - Node Not Found
```bash
curl -X GET "http://127.0.0.1:8000/api/nodes/?by=node_id&value=n999" -H "accept: application/json"
```

**Expected Response (404 Not Found):**
```json
{
  "count": 0,
  "query_params": {
    "by": "node_id",
    "value": "n999"
  },
  "nodes": [],
  "message": "No nodes found matching the specified criteria"
}
```

## Using Python Requests

```python
import requests
import json

base_url = "http://127.0.0.1:8000/api"

# 1. Get node by ID
response = requests.get(f"{base_url}/nodes/", params={"by": "node_id", "value": "n001"})
print(json.dumps(response.json(), indent=2))

# 2. Get nodes by name
response = requests.get(f"{base_url}/nodes/", params={"by": "name", "value": "Alice Johnson"})
print(json.dumps(response.json(), indent=2))

# 3. Get nodes by label
response = requests.get(f"{base_url}/nodes/", params={"by": "label", "value": "Person"})
print(json.dumps(response.json(), indent=2))

# 4. Get all nodes
response = requests.get(f"{base_url}/nodes/all/")
print(json.dumps(response.json(), indent=2))

# 5. Get specific node by ID
response = requests.get(f"{base_url}/nodes/n001/")
print(json.dumps(response.json(), indent=2))
```

## Using JavaScript Fetch

```javascript
const baseUrl = "http://127.0.0.1:8000/api";

// 1. Get node by ID
fetch(`${baseUrl}/nodes/?by=node_id&value=n001`)
  .then(response => response.json())
  .then(data => console.log(data));

// 2. Get nodes by label
fetch(`${baseUrl}/nodes/?by=label&value=Person`)
  .then(response => response.json())
  .then(data => console.log(data));

// 3. Get all nodes
fetch(`${baseUrl}/nodes/all/`)
  .then(response => response.json())
  .then(data => console.log(data));

// 4. Get specific node
fetch(`${baseUrl}/nodes/n001/`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## Postman Collection

Import these requests into Postman:

1. Create a new collection called "Graph Database API"
2. Add the base URL as a variable: `{{base_url}} = http://127.0.0.1:8000/api`
3. Add requests:
   - GET `{{base_url}}/nodes/?by=node_id&value=n001`
   - GET `{{base_url}}/nodes/?by=name&value=Alice Johnson`
   - GET `{{base_url}}/nodes/?by=label&value=Person`
   - GET `{{base_url}}/nodes/all/`
   - GET `{{base_url}}/nodes/n001/`
