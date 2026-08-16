.PHONY: install backend frontend up down

install:
	python -m pip install -r backend/requirements.txt -r frontend/requirements.txt

backend:
	python backend/app.py

frontend:
	streamlit run frontend/app.py --server.port 8501 --server.headless true

up:
	docker-compose up --build

down:
	docker-compose down
