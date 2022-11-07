release: python manage.py migrate && python manage.py createsuperuser --noinput --username admin --email y@gmail.com 
web: gunicorn zwroty.wsgi --log-file -
