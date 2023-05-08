# Just exit safely if a wrong command was used
just_do_nothing_to_save_everything:
	@echo "Something went wrong, just do nothing to avoid any harm..."

# Clear all stuff
clear_all:
	# clear all docker stuff
	make -i clear_docker_containers clear_docker_images clear_docker_system
	# clear files
	make -i clear_db_dumps clear_pyc clear_settings clear_static

# Clear cached database dumps in the admitad project folder
clear_db_dumps:
	@echo "Removing cached SQL dumps..."
	rm ../admitad/test_data/cached_acceptance_db.sql
	rm ../admitad/test_data/cached_schema.sql

# Clear docker containers
clear_docker_containers:
	@echo "Removing docker containers..."
	docker stop $$(docker ps -a -q)
	docker rm $$(docker ps -a -q)

# Clear docker images
clear_docker_images:
	@echo "Removing docker images..."
	# docker rmi $$(docker images -a -q) -f
	docker image prune -af

# Clear all unused docker stuff
clear_docker_system:
	@echo "Starting docker system prune..."
	docker system prune -af

# Clear *.pyc files in the admitad project folder
clear_pyc:
	@echo "Removing *.pyc files..."
	find ../admitad/ -name \*.pyc -delete
# Run flake8 on local environment
flake8:
	@echo "Starting flake8..."
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run flake8

# Run pylint on local environment
pylint:
	@echo "Starting pylint..."
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run make pylint_ci

# Run pylint for all *.py files which were added to repository
PY_FILES := git ls-files '*.py'
pylint_ci:
	pylint --rcfile=.pylintrc --exit-zero `$(PY_FILES)`

# Run pytest with specified tag
COMPOSE_CONFIG := ../admitad/acceptance-infra/acceptance-infra_local.yml
test:
	@echo "Starting tests..."
	docker-compose -f ${COMPOSE_CONFIG} exec monolith-test-p3 pytest -v -s -m ${tag} --headless=no
