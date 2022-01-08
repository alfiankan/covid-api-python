test:
	pytest -v
cover:
	pytest --cov
dev:
	python3 http_server.py
run:
	gunicorn --bind localhost:3000 wsgi:startServer && python3 sync_scheduler.py
install:
	python3 -m pip install -r requirements.txt
