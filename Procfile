release: python manage.py migrate && createsuperuser --noinput --username admin --email y@gmail.com --password 1111
web: gunicorn zwroty.wsgi --log-file -
