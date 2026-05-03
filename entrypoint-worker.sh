#!/bin/bash

set -e

echo "Ожидаем подключение к базе данных для Celery worker..."
python3 -c "
import socket, time, os
host = os.getenv('APP_CONFIG__DB__HOST', 'postgres')
port = int(os.getenv('APP_CONFIG__DB__PORT', '5432'))
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        print('База данных пока недоступна...')
        time.sleep(2)
"

echo "База данных доступна. Запускаем Celery worker без миграций."

exec "$@"
