test:
	pytest -v
cover:
	pytest --cov
dev:
	python3 api.py
run:
	gunicorn --bind localhost:3000 wsgi:startApi && python3 sync_scheduler.py
install:
	python3 -m pip install -r requirements.txt
