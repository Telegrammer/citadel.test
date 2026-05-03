#!/bin/bash

set -e

echo "Ожидаем подключение к базе данных..."
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

echo "База данных доступна."

echo "Запускаем Alembic миграции..."
lock="${ALEMBIC_UPGRADE_LOCK_PATH:-/tmp/alembic-upgrade.lock}"
(
    flock -w 120 9 || exit 1
    alembic -c src/alembic.ini upgrade head
) 9>"${lock}"
echo "Миграции успешно применены."

echo "Запускаем приложение..."
exec "$@"
