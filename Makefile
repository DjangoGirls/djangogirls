all: help

help:
	@echo -n $(blue)
	@echo 'USAGE: make <target>'
	@echo -n $(normal)
	@echo '-------'
	@echo 'Targets'
	@echo '-------'
	@echo '    requirements .................................. install all the required dependencies'
	@echo '    migrate .................................. create the database'
	@echo '    run .................................. run your local server'
	@echo '    event .................................. add a sample event'

requirements:
	@echo 'Installing ./requirements.txt'
	@pip install -r ./requirements.txt

migrate:
	@./manage.py migrate

run:
	@./manage.py runserver

event:
	@./manage.py new_event



