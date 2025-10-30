# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  (Browser, Postman, cURL, Mobile Apps, Other Services)          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API Gateway Layer                            │
│                   (Django URL Router)                           │
│                                                                  │
│  Routes:                                                         │
│  - /swagger/          → Swagger UI                              │
│  - /api/nodes/        → Get Nodes View                          │
│  - /api/nodes/all/    → Get All Nodes View                      │
│  - /api/nodes/{id}/   → Get Node By ID View                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    Presentation Layer                           │
│                  (Django REST Views)                            │
│                                                                  │
│  Components:                                                     │
│  ├── GetNodesView          - Query nodes by criteria           │
│  ├── GetAllNodesView       - Retrieve all nodes                │
│  └── GetNodeByIdView       - Get specific node                 │
│                                                                  │
│  Responsibilities:                                               │
│  - Request handling                                              │
│  - Response formatting                                           │
│  - HTTP status code management                                   │
│  - Error handling                                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Serialization Layer                           │
│                 (DRF Serializers)                               │
│                                                                  │
│  Components:                                                     │
│  ├── NodeQuerySerializer        - Input validation             │
│  ├── NodeDetailSerializer       - Node data structure          │
│  ├── NodeListResponseSerializer - Response format              │
│  └── NodePropertySerializer     - Property validation          │
│                                                                  │
│  Responsibilities:                                               │
│  - Input validation                                              │
│  - Data transformation                                           │
│  - Output serialization                                          │
│  - Type checking                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Business Logic Layer                          │
│                 (Service Classes)                               │
│                                                                  │
│  GraphDatabaseService:                                           │
│  ├── get_nodes_by_criteria()  - Query nodes                    │
│  ├── get_node_by_id()         - Get single node                │
│  └── get_all_nodes()          - Retrieve all nodes             │
│                                                                  │
│  Responsibilities:                                               │
│  - Business logic                                                │
│  - Data access logic                                             │
│  - Query optimization                                            │
│  - Data filtering                                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    Data Layer                                   │
│              (Graph Database / In-Memory)                       │
│                                                                  │
│  Current: Dummy Data (In-Memory)                                │
│  Future: Neo4j, ArangoDB, Neptune, etc.                         │
│                                                                  │
│  Data Structure:                                                 │
│  ├── Nodes (with IDs, Labels, Properties)                      │
│  ├── Relationships (with Types, Properties)                     │
│  └── Metadata (Timestamps, Degrees)                             │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

```
1. Client Request
   │
   ├─► Example: GET /api/nodes/?by=name&value=Alice
   │
   ▼

2. URL Router (urls.py)
   │
   ├─► Matches pattern: /api/nodes/
   ├─► Routes to: GetNodesView
   │
   ▼

3. View Layer (views.py)
   │
   ├─► Extracts query parameters
   ├─► Creates serializer: NodeQuerySerializer(data=query_params)
   ├─► Validates input
   │
   ▼

4. Serialization (serializers.py)
   │
   ├─► Validates 'by' field (must be in allowed list)
   ├─► Validates 'value' field (required string)
   ├─► Returns validated data
   │
   ▼

5. Service Layer (services.py)
   │
   ├─► Calls: GraphDatabaseService.get_nodes_by_criteria()
   ├─► Performs business logic
   ├─► Queries data layer
   │
   ▼

6. Data Layer
   │
   ├─► Searches through DUMMY_NODES
   ├─► Filters by criteria
   ├─► Returns matching nodes
   │
   ▼

7. Response Serialization
   │
   ├─► Wraps data in response format
   ├─► Adds metadata (count, query_params)
   ├─► Serializes to JSON
   │
   ▼

8. HTTP Response
   │
   └─► Returns JSON with status code (200, 404, 400)
```

## Component Interactions

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │ HTTP Request
       ▼
┌──────────────────────┐
│   Django URLs        │
│  (URL Routing)       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐       ┌─────────────────────┐
│   View               │──────►│  Serializer         │
│  - GetNodesView      │◄──────│  - Validation       │
│  - Request handling  │       │  - Data transform   │
└──────┬───────────────┘       └─────────────────────┘
       │
       │ Call service method
       ▼
┌──────────────────────┐
│   Service            │
│  - Business logic    │
│  - Data access       │
└──────┬───────────────┘
       │
       │ Query data
       ▼
┌──────────────────────┐
│   Data Source        │
│  - Dummy data        │
│  - Graph DB (future) │
└──────────────────────┘
```

## Layer Responsibilities

### 1. URL Layer (`urls.py`)
- **Purpose**: Route incoming requests to appropriate views
- **Responsibility**: Map URL patterns to view functions/classes
- **Example**: `/api/nodes/` → `GetNodesView`

### 2. View Layer (`views.py`)
- **Purpose**: Handle HTTP requests and responses
- **Responsibilities**:
  - Extract request parameters
  - Validate input using serializers
  - Call service layer methods
  - Format responses
  - Handle errors
  - Set HTTP status codes

### 3. Serializer Layer (`serializers.py`)
- **Purpose**: Data validation and transformation
- **Responsibilities**:
  - Validate input data
  - Define data schemas
  - Convert data types
  - Custom validation logic
  - Serialize output data

### 4. Service Layer (`services.py`)
- **Purpose**: Implement business logic
- **Responsibilities**:
  - Execute business rules
  - Coordinate data access
  - Perform calculations
  - Filter and transform data
  - Database interaction logic

### 5. Data Layer (Database/Dummy Data)
- **Purpose**: Store and retrieve data
- **Responsibilities**:
  - Data persistence
  - Query execution
  - Data integrity
  - Transaction management

## Design Patterns Used

### 1. **MVC (Model-View-Controller) Pattern**
- **Model**: Serializers + Service Layer
- **View**: Django REST Views
- **Controller**: URL routing

### 2. **Service Layer Pattern**
- Separates business logic from views
- Reusable across multiple views
- Easy to test independently

### 3. **Serializer Pattern**
- Centralized data validation
- Consistent data transformation
- API contract definition

### 4. **Repository Pattern** (Implicit)
- `GraphDatabaseService` acts as repository
- Abstracts data access
- Easy to swap data sources

## API Documentation (Swagger/OpenAPI)

```
┌─────────────────────────────────────┐
│         Swagger UI                  │
│  - Interactive API docs             │
│  - Try it out functionality         │
│  - Schema visualization             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      drf-yasg (OpenAPI)             │
│  - Auto-generate schema             │
│  - Decorators for docs              │
│  - Schema validation                │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      Django REST Views              │
│  - Annotated with swagger_auto_sch  │
│  - Parameter definitions            │
│  - Response examples                │
└─────────────────────────────────────┘
```

## Data Flow Example

### Query: Get nodes by name "Alice Johnson"

```
Request:
GET /api/nodes/?by=name&value=Alice Johnson

Flow:
1. URL Router matches /api/nodes/
2. GetNodesView.get() is called
3. NodeQuerySerializer validates:
   - by = "name" ✓
   - value = "Alice Johnson" ✓
4. GraphDatabaseService.get_nodes_by_criteria("name", "Alice Johnson")
5. Service iterates through DUMMY_NODES
6. Finds node where properties["name"] == "Alice Johnson"
7. Returns matching node(s)
8. View wraps in response format
9. Returns JSON with status 200

Response:
{
  "count": 1,
  "query_params": {"by": "name", "value": "Alice Johnson"},
  "nodes": [{ node data }]
}
```

## Extension Points

### Adding New Query Types
1. Add validation in `NodeQuerySerializer`
2. Update `allowed_fields` list
3. Implement query logic in `GraphDatabaseService`

### Adding New Endpoints
1. Create new view class
2. Add route in `urls.py`
3. Add swagger documentation
4. Implement service method

### Connecting Real Database
1. Install database driver (neo4j, py2neo, etc.)
2. Update `GraphDatabaseService` to use real connection
3. Replace dummy data methods with actual queries
4. Add connection configuration in settings

## Security Considerations

### Current Implementation
- No authentication (demo purposes)
- No rate limiting
- No input sanitization (beyond validation)

### Production Recommendations
- Add authentication (JWT, OAuth2)
- Implement rate limiting
- Add CSRF protection
- Use HTTPS
- Sanitize inputs
- Add logging
- Implement monitoring

## Performance Considerations

### Current Implementation
- In-memory data (very fast)
- No caching
- No pagination (for small datasets)

### Production Recommendations
- Add database connection pooling
- Implement caching (Redis)
- Add pagination for large results
- Use database indexes
- Implement query optimization
- Add response compression
- Use async views for I/O operations

## Testing Strategy

### Unit Tests
- Test serializers independently
- Test service layer methods
- Mock database calls

### Integration Tests
- Test full request/response cycle
- Test error handling
- Test validation

### API Tests
- Test all endpoints
- Test query parameters
- Test edge cases
- Test error responses
