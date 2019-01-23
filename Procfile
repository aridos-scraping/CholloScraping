% Prepare to release
release: sh -c 'cd cholloscraping && python manage.py migrate'
% Launch!
web: sh -c 'cd cholloscraping && gunicorn cholloscraping.wsgi --log-file -'