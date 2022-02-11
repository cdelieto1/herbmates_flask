FLASK_APP=server.py DATADOG_ENV=flask_test ddtrace-run flask run --port=4999 --host=0.0.0.0
