web: gunicorn --pythonpath="/Users/kevinzhang/Desktop/Projects/afou-scraper" config.wsgi:application
worker: python afou-scraper/manage.py rqworker high default low
