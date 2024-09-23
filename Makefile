
On_Green= \033[42m..........
reset = ...........\033[0m


all: down build migrate up

build:
	@ echo "${On_Green}BUILD${reset}"
	docker compose build

up:
	@ echo "${On_Green}UP${reset}"
	docker compose up --build

down:
	@ echo "${On_Green}DOWN${reset}"
	docker compose down

migrate: down
	@ echo "${On_Green}MIGRATE${reset}"
	docker compose run --rm web python3 manage.py makemigrations mysite
	docker compose run --rm web python3 manage.py migrate

static: down
	docker compose run web python3 manage.py collectstatic

train:
	docker compose run web python3 ia_op/iaopp.py