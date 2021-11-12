init:
	pipenv install --deploy
run-flask:
	FLASK_APP=$PWD/app/api/endpoints.py FLASK_ENV=development pipenv run python -m flask run --port 4433
run-react:
	cd app/web/app && npm start
test:
	pytest app/test/
integration:

image:

docker:

dev:

qa:

prod:


