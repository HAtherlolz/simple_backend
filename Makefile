# Variables
COMPOSE_FILE=docker/docker-compose-local.yml
SERVICE=simple_backend
CONTAINER=docker-simple_backend-1

# Targets
.PHONY: lint run down ps build startapp

lint:
	docker-compose -f $(COMPOSE_FILE) run --rm $(SERVICE) sh -c "pylint apps --rcfile=.pylintrc"

run:
	docker-compose -f $(COMPOSE_FILE) up

down:
	docker-compose -f $(COMPOSE_FILE) down

ps:
	docker-compose -f $(COMPOSE_FILE) ps

build:
	docker-compose -f $(COMPOSE_FILE) up --build

startapp:
	@read -p "Enter app name: " app_name && \
	docker exec -it $(CONTAINER) python manage.py startapp $$app_name
