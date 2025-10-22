up:
	docker compose --env-file .env.dev --profile dev up -d

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

restart:
	docker compose restart

clean:
	docker compose down -v --remove-orphans
