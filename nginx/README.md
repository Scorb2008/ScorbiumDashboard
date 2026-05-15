# Nginx в проекте

В этом репозитории nginx настраивается не вручную, а через скрипты проекта.

## Какие файлы используются

- `nginx/nginx.local.conf` — dev-конфиг для локального `docker compose`
- `nginx/nginx.conf` — prod-конфиг

## Кто генерирует `nginx.conf`

- `setup.sh` — при первой прод-установке
- `update.sh` — при каждом обновлении

Из-за этого редактировать `nginx/nginx.conf` руками обычно бессмысленно: скрипт его перезапишет.

## Какой роутинг ожидается

- `/panel/` → админ-панель
- `/api/` → REST API
- `/cabinet/` → пользовательский кабинет
- `/webhook/bot` → Telegram webhook
- `/ws/notifications` → websocket панели

## Локальная разработка

Для dev используется `docker-compose.yml`, который монтирует:

```text
./nginx/nginx.local.conf:/etc/nginx/nginx.conf
```

Обычно панель доступна на:

- [http://localhost/panel/](http://localhost/panel/)

## Продакшен

Для prod используется `docker-compose.prod.yml`, который монтирует:

```text
./nginx/nginx.conf:/etc/nginx/nginx.conf
```

HTTPS-порт берется из `.env` через `HTTPS_PORT`, по умолчанию `443`.

## SSL

Скрипты ожидают сертификаты в одном из путей:

- `nginx/ssl/live/<domain>/fullchain.pem`
- `nginx/ssl/live/<domain>/privkey.pem`

Если сертификаты лежат в `/etc/letsencrypt/live/<domain>/`, `update.sh` умеет их оттуда скопировать.

## Что не забыть

- не редактировать `nginx.conf` вручную перед обычным деплоем
- после смены домена обновить `.env`
- использовать `setup.sh` для первичной настройки и `update.sh` для обновлений
