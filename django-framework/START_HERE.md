# 🚀 START HERE - Django Graph Database API

Welcome! This is a complete Django REST API with Swagger documentation for querying graph database nodes.

## 📖 Quick Navigation

### For Quick Start
👉 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Get started in 2 minutes

### For Complete Guide
👉 **[README.md](README.md)** - Full documentation with setup instructions

### For API Examples
👉 **[EXAMPLES.md](EXAMPLES.md)** - All API calls with responses

### For Understanding Architecture
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and patterns

### For Project Overview
👉 **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What's included

## ⚡ 30-Second Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Start server
python manage.py runserver

# 4. Open browser
http://127.0.0.1:8000/swagger/
```

## 🎯 What Can You Do?

### Query Nodes by Various Criteria
```bash
# By ID
GET /api/nodes/?by=node_id&value=n001

# By Name
GET /api/nodes/?by=name&value=Alice Johnson

# By Label
GET /api/nodes/?by=label&value=Person

# By City
GET /api/nodes/?by=city&value=New York

# By Status
GET /api/nodes/?by=status&value=active
```

### Get All Nodes
```bash
GET /api/nodes/all/
```

### Get Specific Node
```bash
GET /api/nodes/n001/
```

## 📊 Sample Data Available

6 nodes with complete properties:
- Alice Johnson (Person, User) - New York
- Bob Smith (Person, User) - San Francisco  
- Charlie Brown (Person, Admin) - Chicago
- Diana Prince (Person, User) - Boston
- TechCorp Inc (Organization, Company) - Seattle
- Alice Cooper (Person, User) - Los Angeles

## 🌐 Important URLs

After starting the server:

- **Swagger UI** (Interactive docs): http://127.0.0.1:8000/swagger/
- **ReDoc** (Alternative docs): http://127.0.0.1:8000/redoc/
- **API Base**: http://127.0.0.1:8000/api/

## 📁 Project Structure

```
graph_api/
├── 📄 START_HERE.md          ← You are here
├── 📄 QUICK_REFERENCE.md     ← Quick start guide
├── 📄 README.md              ← Complete documentation
├── 📄 EXAMPLES.md            ← API examples
├── 📄 ARCHITECTURE.md        ← System architecture
├── 📄 PROJECT_SUMMARY.md     ← Project overview
│
├── 📄 manage.py              ← Django management
├── 📄 requirements.txt       ← Python dependencies
├── 📄 start.sh               ← Quick start script
│
├── 📁 graph_api/             ← Django project
│   ├── settings.py           ← Configuration
│   └── urls.py               ← URL routing + Swagger
│
└── 📁 graph_nodes/           ← Graph nodes app
    ├── serializers.py        ← Data validation
    ├── services.py           ← Business logic + dummy data
    ├── views.py              ← API endpoints
    └── urls.py               ← App routing
```

## ✨ Key Features

✅ **RESTful API** - Industry standard design
✅ **Swagger UI** - Interactive documentation
✅ **Query Flexibility** - Multiple search criteria
✅ **Clean Architecture** - Layered design
✅ **Dummy Data** - Ready to test
✅ **Full Documentation** - Complete guides

## 🎓 Learning Path

### Beginner
1. Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Run the server
3. Explore Swagger UI
4. Try example queries

### Intermediate
1. Read [README.md](README.md)
2. Review [EXAMPLES.md](EXAMPLES.md)
3. Test all endpoints
4. Modify dummy data

### Advanced
1. Study [ARCHITECTURE.md](ARCHITECTURE.md)
2. Understand the layers
3. Connect real database
4. Add new features

## 🔧 Common Tasks

### Run the Server
```bash
python manage.py runserver
```

### Test an Endpoint
```bash
curl "http://127.0.0.1:8000/api/nodes/?by=city&value=Chicago"
```

### View API Documentation
```
Open browser: http://127.0.0.1:8000/swagger/
```

### Connect Real Database
Edit `graph_nodes/services.py` - see README.md for details

## 💡 Tips

1. **Start with Swagger UI** - It's the easiest way to explore
2. **Try Different Queries** - Test various search criteria
3. **Check Response Format** - Understand the data structure
4. **Read Architecture** - Learn the design patterns
5. **Modify and Extend** - Make it your own!

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Module Not Found
Make sure you're in the project directory and virtual environment is activated

## 📞 API Response Codes

- **200 OK** - Success
- **400 Bad Request** - Invalid parameters
- **404 Not Found** - No results
- **500 Internal Server Error** - Server issue

## 🎯 Next Steps

1. ✅ Start the server
2. ✅ Open Swagger UI
3. ✅ Try the "Get Nodes" endpoint
4. ✅ Query by different criteria
5. ✅ Review the responses
6. ✅ Read the architecture
7. ✅ Extend the API

## 📚 All Documentation Files

| File | Purpose |
|------|---------|
| **START_HERE.md** | This file - Quick orientation |
| **QUICK_REFERENCE.md** | Quick start and common commands |
| **README.md** | Complete setup and usage guide |
| **EXAMPLES.md** | Detailed API examples with responses |
| **ARCHITECTURE.md** | System design and architecture |
| **PROJECT_SUMMARY.md** | Project overview and features |

## 🎉 Ready to Start?

Choose your path:

- **Just want to run it?** → Use `start.sh` or follow Quick Start above
- **Want to understand it?** → Read [README.md](README.md)
- **Need quick reference?** → Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Want to see examples?** → Browse [EXAMPLES.md](EXAMPLES.md)
- **Curious about design?** → Study [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Happy coding! 🚀**

Need help? Check the README.md for detailed information or explore the Swagger UI for interactive documentation.
