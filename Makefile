build:
	docker build --force-rm $(options) -t messed-up-website:latest .

build-prod:
	$(MAKE) build options="--target production"

start:
	docker compose up --remove-orphans $(options) 

stop:
	docker compose down --remove-orphans $(options)

stop-db:
	docker compose down --remove-orphans -v $(options)

create-superuser:
	docker compose run --rm $(options) website uv run manage.py createsuperuser

make-migrations:
	docker compose run --rm $(options) website uv run manage.py makemigrations

manage-py:
	docker compose run --rm $(options) website uv run manage.py $(cmd)
