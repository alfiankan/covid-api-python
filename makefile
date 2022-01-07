test:
	pytest
cover:
	pytest --cov
dev:
	flask run --host=localhost --port=3000 && python3 sync_scheduler.py
run:
	gunicorn --bind localhost:3000 wsgi:app && python3 sync_scheduler.py
install:
	python3 -m pip install -r requirements.txt
