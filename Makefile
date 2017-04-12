.PHONY: clean docs help
.DEFAULT_GOAL := help

ENV := mqtt

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

IMAGE_NAME := $(shell basename $$(pwd))
CONTAINER_NAME := $(shell basename $$(pwd))

PORTS := -p 2500:2500 -p 1100:1100

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
	@echo "IMAGE_NAME = $(IMAGE_NAME)"
	@echo "CONTAINER_NAME = $(CONTAINER_NAME)"

build:  ## Construir el contenedor
	docker build -t $(IMAGE_NAME) .

run:    ## Ejecutar el contenedor
	docker run --name $(CONTAINER_NAME) --rm $(PORTS) $(IMAGE_NAME)

stop:   ## Detener el contenedor
	docker stop $(CONTAINER_NAME)

re:     ## Recrear el contenedor y relanzarlo
	$(MAKE) stop || true
	$(MAKE) build run

shell:
	docker exec -ti -e TERM=xterm $(CONTAINER_NAME) bash




deploy:
	eval $$(docker-machine env $(ENV)) && \
		docker stop $(CONTAINER_NAME) || true
	eval $$(docker-machine env $(ENV)) && \
		docker rm $(CONTAINER_NAME) || true
	eval $$(docker-machine env $(ENV)) && \
		docker build -t $(IMAGE_NAME) . && \
		docker run --restart=unless-stopped --name=$(IMAGE_NAME) -d $(PORTS) $(IMAGE_NAME)