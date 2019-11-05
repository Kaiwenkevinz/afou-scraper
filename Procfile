web: gunicorn afou-scraper.wsgi
web: gunicorn --pythonpath="/Users/kevinzhang/Desktop/Projects/afou-scraper" afou-scraper.wsgi:application
worker: python afou-scraper/manage.py rqworker high default low
