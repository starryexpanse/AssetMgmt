ENVS := POSTGRESQL_DB_URL=postgresql://127.0.0.1:5432/assets

debug:
	$(ENVS) FLASK_DEBUG=1 FLASK_APP=src/main.py flask run

wipe_db:
	$(ENVS) python scripts/create_all.py
