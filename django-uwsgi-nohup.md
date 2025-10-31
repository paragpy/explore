Perfect! Since your Django project structure has `graph_api` as the root folder under `app`, let me update the scripts accordingly:

## **Updated Django API Scripts for graph_api Structure**

### **Step 1: Updated Django uWSGI Config**

```bash
nano /home/emerg1/app/uwsgi_django.ini
```

```ini
[uwsgi]
# Django application settings - updated for graph_api
module = graph_api.wsgi:application
chdir = /home/emerg1/app
pythonpath = /home/emerg1/app

# Process management
master = true
processes = 4
threads = 2
enable-threads = true

# Network binding
http = 0.0.0.0:7000

# Django specific - updated for graph_api
env = DJANGO_SETTINGS_MODULE=graph_api.settings
vacuum = true
die-on-term = true

# Performance
max-requests = 1000
max-requests-delta = 100
harakiri = 300
buffer-size = 32768

# Logging
logto = /home/emerg1/app/logs/django_uwsgi.log
log-maxsize = 50000000
log-date = true
log-level = info

# Static files
static-map = /static=/home/emerg1/app/static
static-expires-uri = /static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf) 315360000
```

### **Step 2: Updated Django Startup Script**

```bash
nano /home/emerg1/app/start_django_nohup.sh
```

```bash
#!/bin/bash
set -e

echo "Starting Django Graph API deployment..."

# Navigate to Django app directory
cd /home/emerg1/app

# Activate virtual environment
source /home/emerg1/.venv/bin/activate

# Ensure logs directory exists
mkdir -p logs

# Export Django settings and Python path for graph_api
export DJANGO_SETTINGS_MODULE=graph_api.settings
export PYTHONPATH="/home/emerg1/app:$PYTHONPATH"

# Check if manage.py exists
if [ ! -f manage.py ]; then
    echo "Error: manage.py not found in /home/emerg1/app"
    exit 1
fi

# Run Django management commands
echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating Django superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
" || true

# Start Django Graph API with uWSGI using nohup
echo "Starting Django Graph API with uWSGI..."
nohup uwsgi --ini uwsgi_django.ini > logs/django_startup.log 2>&1 &

# Get the PID
DJANGO_PID=$!
echo $DJANGO_PID > logs/django.pid

echo "================================"
echo "Django Graph API started successfully!"
echo "PID: $DJANGO_PID"
echo "URL: http://10.198.52.64:7000"
echo "Admin: http://10.198.52.64:7000/admin"
echo "API Docs: http://10.198.52.64:7000/api/"
echo "Graph API: http://10.198.52.64:7000/graph/"
echo "================================"
echo "Useful commands:"
echo "  View logs: tail -f /home/emerg1/app/logs/django_uwsgi.log"
echo "  Check process: ps aux | grep uwsgi"
echo "  Stop app: ./stop_django.sh"
echo "================================"
```

### **Step 3: Updated Django Stop Script**

```bash
nano /home/emerg1/app/stop_django.sh
```

```bash
#!/bin/bash

echo "Stopping Django Graph API..."

cd /home/emerg1/app

# Stop using PID file
if [ -f logs/django.pid ]; then
    PID=$(cat logs/django.pid)
    echo "Stopping Django Graph API (PID: $PID)..."
    kill $PID 2>/dev/null || true
    rm logs/django.pid
    echo "Django Graph API stopped via PID."
else
    echo "No PID file found."
fi

# Also kill any Django uwsgi processes for this user
echo "Cleaning up any remaining uwsgi processes..."
pkill -f "uwsgi.*graph_api.wsgi" || true
pkill -f "uwsgi.*7000" || true

# Check if any processes are still running
REMAINING=$(ps aux | grep -E "(uwsgi.*7000|uwsgi.*graph_api.wsgi)" | grep -v grep | wc -l)
if [ $REMAINING -eq 0 ]; then
    echo "Django Graph API stopped successfully."
else
    echo "Warning: Some uwsgi processes may still be running."
    ps aux | grep -E "(uwsgi.*7000|uwsgi.*graph_api.wsgi)" | grep -v grep
fi
```

### **Step 4: Updated Django Management Script**

```bash
nano /home/emerg1/app/manage_django.sh
```

```bash
#!/bin/bash

cd /home/emerg1/app
source /home/emerg1/.venv/bin/activate

# Set Django settings for graph_api
export DJANGO_SETTINGS_MODULE=graph_api.settings

case $1 in
    start)
        echo "Starting Django Graph API..."
        ./start_django_nohup.sh
        ;;
    stop)
        echo "Stopping Django Graph API..."
        ./stop_django.sh
        ;;
    restart)
        echo "Restarting Django Graph API..."
        ./stop_django.sh
        sleep 3
        ./start_django_nohup.sh
        ;;
    status)
        echo "Django Graph API Status:"
        if [ -f logs/django.pid ]; then
            PID=$(cat logs/django.pid)
            if ps -p $PID > /dev/null; then
                echo "✓ Running (PID: $PID)"
                echo "✓ URL: http://10.198.52.64:7000"
            else
                echo "✗ PID file exists but process not running"
            fi
        else
            echo "✗ Not running (no PID file)"
        fi
        
        # Check listening ports
        if netstat -tlnp 2>/dev/null | grep -q :7000; then
            echo "✓ Port 7000 is listening"
        else
            echo "✗ Port 7000 is not listening"
        fi
        ;;
    logs)
        echo "Viewing Django Graph API logs (Press Ctrl+C to exit):"
        tail -f logs/django_uwsgi.log
        ;;
    shell)
        echo "Opening Django shell..."
        python manage.py shell
        ;;
    migrate)
        echo "Running Django migrations..."
        python manage.py migrate
        ;;
    test)
        echo "Testing Django Graph API..."
        curl -s http://localhost:7000/ | head -20
        echo ""
        echo "Graph API test completed."
        ;;
    dbshell)
        echo "Opening Django database shell..."
        python manage.py dbshell
        ;;
    *)
        echo "Django Graph API Management Script"
        echo "Usage: $0 {start|stop|restart|status|logs|shell|migrate|test|dbshell}"
        echo ""
        echo "Commands:"
        echo "  start   - Start Django Graph API"
        echo "  stop    - Stop Django Graph API"
        echo "  restart - Restart Django Graph API"
        echo "  status  - Check if API is running"
        echo "  logs    - View real-time logs"
        echo "  shell   - Open Django shell"
        echo "  migrate - Run database migrations"
        echo "  test    - Test API endpoint"
        echo "  dbshell - Open database shell"
        ;;
esac
```

### **Step 5: Updated Setup Check Script**

```bash
nano /home/emerg1/app/check_django_setup.sh
```

```bash
#!/bin/bash

echo "Checking Django Graph API setup..."

cd /home/emerg1/app
source /home/emerg1/.venv/bin/activate

# Set Django settings
export DJANGO_SETTINGS_MODULE=graph_api.settings

# Check if Django is installed
echo "1. Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')" || {
    echo "Django not found. Installing..."
    pip install django djangorestframework uwsgi
}

# Check if manage.py exists
echo "2. Checking manage.py..."
if [ -f manage.py ]; then
    echo "✓ manage.py found"
else
    echo "✗ manage.py not found in /home/emerg1/app"
    exit 1
fi

# Check if graph_api directory exists
echo "3. Checking graph_api directory..."
if [ -d graph_api ]; then
    echo "✓ graph_api directory found"
    if [ -f graph_api/settings.py ]; then
        echo "✓ graph_api/settings.py found"
    else
        echo "✗ graph_api/settings.py not found"
        exit 1
    fi
    if [ -f graph_api/wsgi.py ]; then
        echo "✓ graph_api/wsgi.py found"
    else
        echo "✗ graph_api/wsgi.py not found"
        exit 1
    fi
else
    echo "✗ graph_api directory not found in /home/emerg1/app"
    exit 1
fi

# Check Django settings
echo "4. Checking Django settings..."
python manage.py check --deploy || {
    echo "Django check failed. Continuing anyway..."
}

# Check database
echo "5. Checking database..."
python -c "
import django
django.setup()
from django.db import connection
print(f'Database: {connection.settings_dict[\"ENGINE\"]}')
" || echo "Database check failed, but continuing..."

# Check if uWSGI is available
echo "6. Checking uWSGI..."
uwsgi --version || {
    echo "uWSGI not found. Installing..."
    pip install uwsgi
}

echo "✓ Django Graph API setup check completed!"
echo ""
echo "Expected directory structure:"
echo "/home/emerg1/app/"
echo "├── manage.py"
echo "├── graph_api/"
echo "│   ├── __init__.py"
echo "│   ├── settings.py"
echo "│   ├── urls.py"
echo "│   └── wsgi.py"
echo "└── [other apps/modules]"
```

### **Make All Scripts Executable**

```bash
cd /home/emerg1/app
chmod +x start_django_nohup.sh
chmod +x stop_django.sh
chmod +x manage_django.sh
chmod +x check_django_setup.sh
```

## **Usage for Your graph_api Structure**

### **Start the Graph API**

```bash
cd /home/emerg1/app

# Check setup first
./check_django_setup.sh

# Start the API
./manage_django.sh start

# Or use direct start
./start_django_nohup.sh
```

### **Test the Graph API**

```bash
# Check status
./manage_django.sh status

# Test the API
curl http://localhost:7000/
curl http://10.198.52.64:7000/

# View logs
./manage_django.sh logs
```

## **Expected Directory Structure**

```
/home/emerg1/app/
├── manage.py
├── graph_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── [other graph_api files]
├── logs/                    # Created automatically
├── static/                  # Django static files
├── uwsgi_django.ini
├── start_django_nohup.sh
├── stop_django.sh
├── manage_django.sh
└── check_django_setup.sh
```

The scripts are now configured for your `graph_api` project structure and will run on **http://10.198.52.64:7000**!