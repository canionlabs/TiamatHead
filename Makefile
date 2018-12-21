ff:
	# docker-compose run -e DJANGO_SETTINGS_MODULE=tiamat_head.settings.tests --no-deps --rm web sh -c "./manage.py makemigrations && ./manage.py migrate && py.test -vx"
	docker-compose run -e DJANGO_SETTINGS_MODULE=tiamat_head.settings.tests --no-deps --rm web sh -c "./manage.py migrate && py.test -vx"

tests:
	docker-compose run -e DJANGO_SETTINGS_MODULE=tiamat_head.settings.tests --no-deps --rm web sh -c "./manage.py makemigrations && ./manage.py migrate && py.test"

run:
	docker-compose up