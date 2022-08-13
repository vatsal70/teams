web: gunicorn ems.wsgi --log-file - 
worker: celery -A ems worker -l info -B