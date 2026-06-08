#cd backend-django
#source .venv/bin/activate
#python manage.py init_default_connection




curl -fsS \
  -X POST \
  http://localhost:18071/api/connections/3/diagnostics-history/ \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 5,
    "delay_ms": 500
  }'