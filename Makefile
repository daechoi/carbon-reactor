REVISION = $(shell git rev-parse HEAD)
export START_TIME:=$(shell date -u +%s)

help:
	@echo "help\t\tPrint this help"
	@echo "build\t\tBuild Docker images"
	@echo "up\t\tStart Docker containers defined in docker-compose.yml"
	@echo "down\t\tStop Docker containers"
	@echo "clean\t\tRemove dangling images and exited containers"
	@echo "clean_volumes\tPrunes volumes"
	
elapsed_time:
	@echo "$$(( `date -u +%s` - $(START_TIME) )) seconds elapsed"

build:
	@docker-compose build
	@make elapsed_time
	@echo "All built 🏛"

up:
	@docker-compose up -d
	@docker-compose logs --tail 10 -f

down:
	@docker-compose stop

clean:
	@echo "Deleting exited containers..."
	@docker ps -a -q -f status=exited | xargs docker rm -v
	@echo "Deleting dangling images..."
	@docker images -q -f dangling=true | xargs docker rmi
	@make elapsed_time
	@echo "All clean 🛀"

clean_volumes:
	@echo "Prune volumes (WARNING: includes your existing database volume if your containers are stopped)..."
	@docker volume prune
	@make elapsed_time
	@echo "All clean 🛀"

