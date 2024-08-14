# Платформа аннотирования видео VisionDataForge

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/) [![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)]() [![Cookies](https://img.shields.io/badge/-Cookies-464646?style=flat-square&logo=Cookies)]() [![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)]() [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/) [![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/) [![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/) [![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/) [![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)

## Описание

Палтформа аннотирования видео

### Доступный функционал

- Регистрация пользователей с помощью библиотеки fastapi-users.
- Аутентификация реализована с помощью куков и JWT-токена.
- Создание датасетов разрешено толька авторизованным пользователям
- Возможность получения подробной информации о себе.
- Возможность развернуть проект в Docker-контейнерах.

#### Технологии

- Python 3.12
- FastAPI
- Асинхронность
- JWT
- Alembic
- SQLAlchemy
- Docker
- PostgreSQL
- Asyncpg
- Uvicorn

#### Локальный запуск проекта

- Склонировать репозиторий:
```bash
git clone https://github.com/lnikioffic/VisionDataForge.git
```

- Установка библиотек:
```bash
python -m pip install -r requirements/requirements.txt 
```
на Linux torch CUDA установиться сам если есть CUDA драйвера


- Файл окружения `.env`. Создать файл `.env` по образцу `env-example`:
```bash
    touch .env
```

- Установка CUDA для Windows:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

- Генерация ключей для JWT:
```bash
mkdir certs && cd certs && openssl genrsa -out jwt-private.pem 2048 && \
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

```
- Создайте базу данных под названием `Forge`

- Применение миграции:
```bash
alembic upgrade head
```

- Запуск проекта:
```shell
uvicorn src.main:app --reload
```

#### Запуск в контейнерах Docker

- Находясь в главной директории проекта:

- Создать файл `.env` по образцу `.env-example-docker`:

```bash
   touch .env 
```

- Запустить проект:

``` bash
    docker-compose up -d --build  
```