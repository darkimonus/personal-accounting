-include env.django
export $(shell sed 's/=.*//' env.django )

runargs :=

.DEFAULT_GOAL := help

SERVICE_NAME := accounting-wsgi

PROJECT_DIR ?= /app


dc := docker compose
dr := $(dc) run --rm $(SERVICE_NAME)


SHELL:=bash

OSFLAG :=
ifeq ($(OS),Windows_NT)
	OSFLAG += WIN32
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OSFLAG += LINUX
	endif
	ifeq ($(UNAME_S),Darwin)
		OSFLAG += OSX
	endif
endif

ifneq (,$(findstring $(firstword $(MAKECMDGOALS)),start-app django-manage))
    runargs := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
    $(eval $(runargs): ; @true)
endif


ifneq ($(DJANGO_PROJECT_NAME),)
$(info Info: Current Django project is: $(DJANGO_PROJECT_NAME))
else
$(info Info: Current Django project is: None)
endif

.PHONY: build
build-app: ## BUILD: Build Django containers and run it
	@printf "$$BGreen Build containers (time for a coffee break ☕ !) $$ColorOff \n"
	@echo "VENV_PATH is: $(VENV_PATH)"
	$(dc) up -d --build

.PHONY: up
up: ## RUN: Run Django containers
	@printf "$$BGreen Build containers (time for a coffee break ☕ !) $$ColorOff \n"
	$(dc) up -d


.PHONY: stop
stop: ## RUN: STOP containers
	@printf "$$BGreen Stopping containers (time for a coffee break ☕ !) $$ColorOff \n"
	$(dc) stop

.PHONY: restart
restart: ## RUN: STOP containers
	@printf "$$BGreen Restarting containers... $$ColorOff \n"
	$(dc) stop
	$(dc) up -d

.PHONY: manage
manage: ## RUN: Execute Django manage.py command [required command args]
ifneq ($(runargs), )
    ifneq ($(SOURCE_FOLDER),)
        ifneq ($(SERVICE_NAME), )
	        docker exec -it $(SERVICE_NAME) poetry run python3 manage.py $(runargs)
        else
	        @printf "$$BGreen Unable to execute command, Docker container is not specified! $$ColorOff \n"
        endif
    else
	    @printf "$$BGreen Unable to create app, Django project is not exist! $$ColorOff \n"
    endif
else
	@printf "$$BGreen Unable to execute manage.py, you need to set the command arguments as a parameter! $$ColorOff \n"
endif

.PHONY: logs
logs: ## RUN: docker-compose stop
	docker logs $(SERVICE_NAME)