## YaMDB
### Описание: ###

Проект YaMDb (REST API) собирает отзывы пользователей на различные произведения.  
Реализовано на `Djangorestframework 3.12.4` Аутентификация на основе `JWT`. Читать контент могут все, вносить и изменять только аутентифицированные пользователи.  
Предоставляет ответы от сервера в формате JSON для последующей сериалиализации на стороне фронта.  
Это первый совместный проект, было сложно но интересно. 

## Установка: ##

### Клонируйте репозиторий: ###

    git clone git@github.com:KitKat-ru/yamdb_final.git


### Пример файла `.env`. Должен находится в папке `./yamdb_final/infra/`: ###
### Такие же `Secrets` должны быть созданы в `GitHub Actions`: ###

    DOCKER_USERNAME=... (имя пользователя (не логин) на DockerHub)
    LOGIN_DOCKER=... (логин пользователя на DockerHub)
    PASSWORD_DOCKER=... (пароль пользователя на DockerHub)

    SSH_KEY=... (ssh ключ указанный для ВМ)
    PASSPHRASE=... (пароль на ssh ключе)
    HOST=... (IP ВМ)
    USER=... (логин в ВМ)

    TELEGRAM_TO=... (ID чата в телеграмме)
    TELEGRAM_TOKEN=... (TOKEN бота в телеграмме)

    SECRET_KEY=... (ключ к Джанго проекту)
    DB_ENGINE=django.db.backends.postgresql (указываем, что работаем с postgresql)
    DB_NAME=postgres (имя базы данных)
    POSTGRES_USER=... (логин для подключения к базе данных)
    POSTGRES_PASSWORD=... (пароль для подключения к БД (установите свой)
    DB_HOST=db (название сервиса (контейнера)
    DB_PORT=5432 (порт для подключения к БД)

### Перейдите в репозиторий к директории с файлами `docker-compose.yaml` и `nginx/default.conf` с помощью командной строки: ###
### В файле `nginx/default.conf` укажите IP ВМ на которой будет запускаться проект ###

    nano yamdb_final/infra/nginx/default.conf

### Скопируйте файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно ###

  
### Подготовьте ВМ. Остановите службу nginx. Установите - [Docker и Docker-compose](https://docs.docker.com/engine/install/ubuntu/): ###

    sudo apt update
    sudo apt upgrade
    sudo systemctl stop nginx
    sudo apt install docker.io

### При использовании команды `git push` запуститься `GitHub Actions` и задеплоит проект на вашу ВМ: ###
    git add .
    git commit -m 'you_text'
    git push

### После развертывания проекта заходите в ВМ и создайте миграции и заполнените базу данных: ###

    sudo docker-compose exec web python manage.py makemigrates
    sudo docker-compose exec web python manage.py migrate
    sudo docker-compose exec web python manage.py createsuperuser
    sudo docker-compose exec web python manage.py collectstatic --no-input

## Алгоритм регистрации пользователей ##
  
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.  
2. YaMDB отправляет письмо с кодом подтверждения `confirmation_code` на адрес `email`. В проекте реализован бэкенд почтового сервиса, папка - `sent_emails`.  

#### - Получаем ключ авторизации для получения токена:

    sudo docker-compose exec web bash
    cd send_emails
    cat "файл с почтой" - копируем confirmation_code

4. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).  
5. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.  

### Для тестирования можно обратиться по `URL`:
    http://551.250.97.9/api/v1/
    http://51.250.97.9/admin/
    http://51.250.97.9/redoc/

### Автор:

- #### [Фабриков Артем](https://github.com/KitKat-ru)

### Лицензия:
- Этот проект лицензируется в соответствии с лицензией MIT ![](https://miro.medium.com/max/156/1*A0rVKDO9tEFamc-Gqt7oEA.png "1")

## Образ выложен на DockerHub, что бы его скачать введите:
    sudo docker pull taeray/taeray/yamdb_web:v.1.0


## Плашка о прохождении `workflow`:
![example workflow](https://github.com/KitKat-ru/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
