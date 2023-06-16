help:
	@echo "dev"
	@echo "prod"
	@echo "re-dev"
	@echo "re-prod"
	@echo "down"
	@echo "ps"
	@echo "local"

dev:
	docker-compose -fdocker-compose.yml -fdev.yml --env-file=dev.env up -d

prod:
	docker-compose --env-file=prod.env up -d

down:
	docker-compose -fdocker-compose.yml -fdev.yml down

ps:
	docker-compose -fdocker-compose.yml -fdev.yml ps

re-dev: down dev
re-prod: down prod

local:
	docker-compose -fdocker-compose.yml -fdev.yml up -d app db adminer
