Perfect! Here are the complete scripts for running a Django API using the same nohup + uWSGI approach on port 7000:

## **Django API Deployment Scripts**

### **Step 1: Create Django uWSGI Config**

```bash
nano /home/emerg1/app/uwsgi_django.ini
```

```ini
[uwsgi]
# Django application settings
module = app.wsgi:application
chdir = /home/emerg1/app
pythonpath = /home/emerg1/app

# Process management
master = true
processes = 4
threads = 2
enable-threads = true

# Network binding
http = 0.0.0.0:7000

# Django specific
env = DJANGO_SETTINGS_MODULE=app.settings
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

# Static files (if needed)
static-map = /static=/home/emerg1/app/static
static-expires-uri = /static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf) 315360000
```

### **Step 2: Create Django Startup Script**

```bash
nano /home/emerg1/app/start_django_nohup.sh
```

```bash
#!/bin/bash
set -e

echo "Starting Django API deployment..."

# Navigate to Django app directory
cd /home/emerg1/app

# Activate virtual environment
source /home/emerg1/.venv/bin/activate

# Ensure logs directory exists
mkdir -p logs

# Export Django settings and Python path
export DJANGO_SETTINGS_MODULE=app.settings
export PYTHONPATH="/home/emerg1/app:$PYTHONPATH"

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

# Start Django with uWSGI using nohup
echo "Starting Django API with uWSGI..."
nohup uwsgi --ini uwsgi_django.ini > logs/django_startup.log 2>&1 &

# Get the PID
DJANGO_PID=$!
echo $DJANGO_PID > logs/django.pid

echo "================================"
echo "Django API started successfully!"
echo "PID: $DJANGO_PID"
echo "URL: http://10.198.52.64:7000"
echo "Admin: http://10.198.52.64:7000/admin"
echo "API Docs: http://10.198.52.64:7000/api/"
echo "================================"
echo "Useful commands:"
echo "  View logs: tail -f /home/emerg1/app/logs/django_uwsgi.log"
echo "  Check process: ps aux | grep uwsgi"
echo "  Stop app: ./stop_django.sh"
echo "================================"
```

Make it executable:

```bash
chmod +x /home/emerg1/app/start_django_nohup.sh
```

### **Step 3: Create Django Stop Script**

```bash
nano /home/emerg1/app/stop_django.sh
```

```bash
#!/bin/bash

echo "Stopping Django API..."

cd /home/emerg1/app

# Stop using PID file
if [ -f logs/django.pid ]; then
    PID=$(cat logs/django.pid)
    echo "Stopping Django API (PID: $PID)..."
    kill $PID 2>/dev/null || true
    rm logs/django.pid
    echo "Django API stopped via PID."
else
    echo "No PID file found."
fi

# Also kill any Django uwsgi processes for this user
echo "Cleaning up any remaining uwsgi processes..."
pkill -f "uwsgi.*app.wsgi" || true
pkill -f "uwsgi.*7000" || true

# Check if any processes are still running
REMAINING=$(ps aux | grep -E "(uwsgi.*7000|uwsgi.*app.wsgi)" | grep -v grep | wc -l)
if [ $REMAINING -eq 0 ]; then
    echo "Django API stopped successfully."
else
    echo "Warning: Some uwsgi processes may still be running."
    ps aux | grep -E "(uwsgi.*7000|uwsgi.*app.wsgi)" | grep -v grep
fi
```

Make it executable:

```bash
chmod +x /home/emerg1/app/stop_django.sh
```

### **Step 4: Create Django Management Script**

```bash
nano /home/emerg1/app/manage_django.sh
```

```bash
#!/bin/bash

cd /home/emerg1/app
source /home/emerg1/.venv/bin/activate

case $1 in
    start)
        echo "Starting Django API..."
        ./start_django_nohup.sh
        ;;
    stop)
        echo "Stopping Django API..."
        ./stop_django.sh
        ;;
    restart)
        echo "Restarting Django API..."
        ./stop_django.sh
        sleep 3
        ./start_django_nohup.sh
        ;;
    status)
        echo "Django API Status:"
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
        echo "Viewing Django logs (Press Ctrl+C to exit):"
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
        echo "Testing Django API..."
        curl -s http://localhost:7000/ | head -20
        echo ""
        echo "API test completed."
        ;;
    *)
        echo "Django API Management Script"
        echo "Usage: $0 {start|stop|restart|status|logs|shell|migrate|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start Django API"
        echo "  stop    - Stop Django API"
        echo "  restart - Restart Django API"
        echo "  status  - Check if API is running"
        echo "  logs    - View real-time logs"
        echo "  shell   - Open Django shell"
        echo "  migrate - Run database migrations"
        echo "  test    - Test API endpoint"
        ;;
esac
```

Make it executable:

```bash
chmod +x /home/emerg1/app/manage_django.sh
```

### **Step 5: Create Django Requirements Check Script**

```bash
nano /home/emerg1/app/check_django_setup.sh
```

```bash
#!/bin/bash

echo "Checking Django setup..."

cd /home/emerg1/app
source /home/emerg1/.venv/bin/activate

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

# Check Django settings
echo "3. Checking Django settings..."
python manage.py check --deploy || {
    echo "Django check failed. Continuing anyway..."
}

# Check database
echo "4. Checking database..."
python -c "
import django
django.setup()
from django.db import connection
print(f'Database: {connection.settings_dict[\"ENGINE\"]}')
"

# Check if uWSGI is available
echo "5. Checking uWSGI..."
uwsgi --version || {
    echo "uWSGI not found. Installing..."
    pip install uwsgi
}

echo "✓ Django setup check completed!"
```

Make it executable:

```bash
chmod +x /home/emerg1/app/check_django_setup.sh
```

## **Usage Instructions**

### **Step 1: Setup and Check Environment**

```bash
# Check Django setup
cd /home/emerg1/app
./check_django_setup.sh
```

### **Step 2: Start Django API**

```bash
# Start the Django API
./manage_django.sh start

# Or use the direct start script
./start_django_nohup.sh
```

### **Step 3: Test the API**

```bash
# Check status
./manage_django.sh status

# Test the API
curl http://localhost:7000/
curl http://10.198.52.64:7000/

# View logs
./manage_django.sh logs
```

### **Step 4: Manage the API**

```bash
# Restart
./manage_django.sh restart

# Stop
./manage_django.sh stop

# Check status
./manage_django.sh status

# Run migrations
./manage_django.sh migrate

# Open Django shell
./manage_django.sh shell
```

## **Firewall Configuration**

```bash
# Open port 7000 for Django API
sudo firewall-cmd --add-port=7000/tcp --permanent
sudo firewall-cmd --reload

# Check if port is open
sudo firewall-cmd --list-ports
```

## **Auto-Start on Boot (Optional)**

```bash
# Add to crontab for auto-start
crontab -e

# Add this line:
@reboot /home/emerg1/app/start_django_nohup.sh
```

## **Directory Structure Expected**

```
/home/emerg1/app/
├── manage.py
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── logs/                    # Created automatically
├── static/                  # Django static files
├── uwsgi_django.ini
├── start_django_nohup.sh
├── stop_django.sh
├── manage_django.sh
└── check_django_setup.sh
```

This setup will run your Django API on **http://10.198.52.64:7000** and handle all Django-specific requirements including migrations, static files, and proper WSGI configuration!