release: python manage.py migrate && python manage.py createsuperuser --noinput --username admin1 --email y1@gmail.com 
web: gunicorn zwroty.wsgi --log-file -
