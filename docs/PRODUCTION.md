PRODUCTION NOTES
================

Коротко
-------
Рекомендуемая production-структура: Docker + gunicorn + nginx. Для sqlite используйте single-worker gunicorn или переходите на Postgres для concurrency.

Gunicorn
--------
- Базовая команда:

  gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 1

- Для SQLite указать `--workers 1`.

Nginx
-----
- Nginx как reverse-proxy перед gunicorn, обслуживает статику. Пример конфигурации:

  server {
      listen 80;
      server_name example.com;

      location /static/ {
          alias /path/to/project/staticfiles/;
      }

      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
+          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }

SSL
---
- Используйте certbot для получения сертификатов и настройте редирект с HTTP на HTTPS.

База данных
-----------
- SQLite не подходит для высоконагруженных многопроцессных окружений.
- Для production рекомендуется перейти на Postgres. Если остаётесь на sqlite — используйте один worker и делайте бэкапы файла `./data/db.sqlite3`.

Systemd + docker-compose
------------------------
- Создайте systemd unit, который запускает `docker-compose up -d` и перезапускается при падении.
- Регулярно бэкапьте `./data/db.sqlite3` и копируйте заархивированные копии на удалённое хранилище.

Backups
-------
- Простейший script:

  #!/bin/sh
  tar czf /backup/quotes-db-$(date +%F).tgz ./data/db.sqlite3

CI/CD
-----
- Добавьте шаги для запуска `pytest` и `flake8` при PR.

Security
--------
- Секреты храните через ENV или секретный менеджер, не в репозитории.
- Отключите DEBUG в production.

*** End Patch
