webapp:
	. venv/bin/activate && PYTHONPATH="${PYTHONPATH}:${PWD}/disboard" DISBOARD_CONF_DIR="${PWD}/priv" uvicorn disboard.webapp:app --reload
