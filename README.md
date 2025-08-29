# Quotes — simple Django service

Коротко
-------
Небольшой сервис для хранения и выдачи цитат с взвешенным случайным выбором, лайками/дизлайками и ограничением числа цитат на источник.

Как собрать и запустить
-----------------------
В корне проекта (где `docker-compose.yml`):

```powershell
docker-compose up --build -d
```

Проверить логи контейнера:

```powershell
docker-compose logs -f
```

docker-compose up --build -d
---------------------------
Миграции выполняются автоматически в entrypoint при старте контейнера. Чтобы создать суперпользователя вручную:

Опционально: показать приложение публично через ngrok (без покупки домена)
-----------------------------------------------------------------

Если нужно временно показать приложение извне для демонстрации или тестирования, можно запустить контейнер ngrok вместе с приложением. В репозитории добавлён сервис `ngrok` в `docker-compose.yml`.

1. Получите authtoken на https://dashboard.ngrok.com/get-started/your-authtoken и пропишите его в `.env` как `NGROK_AUTHTOKEN` (или экспортируйте в окружение).

2. Запустите контейнеры (ngrok зависит от сервиса `web`):

```powershell
docker-compose up --build -d
```

3. После старта ngrok создаст публичный URL, который проксирует `web:8000`. Найти публичный адрес можно:

- в логах сервиса ngrok (в терминале);
- на локальной панели ngrok: http://localhost:4040/status (или http://127.0.0.1:4040).

4. Для получения URL программно используйте локальное API ngrok:

```powershell
# Вернёт JSON со списком туннелей; публичный адрес находится в tunnels[0].public_url
curl http://localhost:4040/api/tunnels | jq .
# В PowerShell можно так:
(Invoke-RestMethod http://localhost:4040/api/tunnels).tunnels[0].public_url
```

Заметки по безопасности
----------------------
- ngrok делает ваше приложение публичным — используйте только для демонстраций или краткосрочных показов. Не публикуйте секреты и чувствительные данные.
- При демонстрации рекомендуется выставлять `DEBUG=False` в окружении.
- Для постоянного публичного адреса лучше настроить собственный домен и TLS; описанный выше способ — для временных показов.
```powershell
docker-compose exec web python src/manage.py createsuperuser
```

SQLite база
-----------
Файл базы находится в репозитории: `./data/db.sqlite3` (монтируется в контейнер как `/app/data/db.sqlite3`).

Эндпоинты и проверка (curl)
---------------------------
1) GET /random — получить одну случайную цитату

```bash
curl http://localhost:8000/random/
```

2) POST /quotes/<id>/like — поставить лайк (CSRF защищено)

# Пример (bash): сначала возьмём CSRF cookie, затем отправим POST с заголовком X-CSRFToken
```bash
curl -c cookies.txt http://localhost:8000/random/ -s
TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -b cookies.txt -H "X-CSRFToken: $TOKEN" -X POST http://localhost:8000/like/1/
```

Если у вас Windows PowerShell, можно открыть страницу в браузере и отправлять POST через форму, либо использовать инструменты, которые умеют работать с cookies/headers.

3) POST /add — добавить цитату (form-data)

Пример (bash):
```bash
curl -c cookies.txt http://localhost:8000/add/ -s
TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -b cookies.txt -H "X-CSRFToken: $TOKEN" -F "text=Hello world" -F "source=me" -F "weight=1.5" http://localhost:8000/add/
```

4) GET /top — топ-10 по лайкам

```bash
curl http://localhost:8000/top/
```

Замечание про URLы
------------------
В приложении маршруты настроены как `/random/`, `/top/`, `/add/`, `/like/<id>/`, `/dislike/<id>/` и `/` (редирект на random).

Тесты
-----
Запуск тестов внутри контейнера:

```powershell
docker-compose exec web pytest -q
```

Где искать конфиг
-----------------
Конфигурация по умолчанию: `config/config.yml`. Значения можно переопределить через ENV — приоритет ENV > YAML > дефолты.

Примеры полезных ENV (см. `.env.example`):

# Quotes — simple Django service

Коротко
-------
Небольшой сервис для хранения и выдачи цитат с взвешенным случайным выбором, лайками/дизлайками и ограничением числа цитат на источник.

Как собрать и запустить
-----------------------
В корне проекта (где находится `docker-compose.yml`):

```powershell
docker-compose up --build -d
```

Проверить логи контейнера (например, для проверки миграций и collectstatic):

```powershell
docker-compose logs -f
```

Миграции и суперпользователь
---------------------------
Миграции выполняются автоматически в entrypoint при старте контейнера. Чтобы создать суперпользователя вручную:

```powershell
docker-compose exec web python src/manage.py createsuperuser
```

SQLite база
-----------
Файл базы находится в репозитории: `./data/db.sqlite3` (монтируется в контейнер как `/app/data/db.sqlite3`). Рекомендуется делать регулярные бэкапы.

Эндпоинты и проверка (curl)
---------------------------
1) GET /random — получить одну случайную цитату

```bash
curl http://localhost:8000/random/
```

2) POST /like/<id>/ — поставить лайк (CSRF защищено)

Пример (bash):
```bash
# получить страницу чтобы сохранить cookie и CSRF
curl -c cookies.txt http://localhost:8000/random/ -s
TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -b cookies.txt -H "X-CSRFToken: $TOKEN" -X POST http://localhost:8000/like/1/
```

3) POST /add — добавить цитату (form-data)

Пример (bash):
```bash
curl -c cookies.txt http://localhost:8000/add/ -s
TOKEN=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -b cookies.txt -H "X-CSRFToken: $TOKEN" -F "text=Hello world" -F "source=me" -F "weight=1.5" http://localhost:8000/add/
```

4) GET /top — топ-10 по лайкам

```bash
curl http://localhost:8000/top/
```

Примечание по URL
-----------------
Маршруты: `/random/`, `/top/`, `/add/`, `/like/<id>/`, `/dislike/<id>/` и `/` (редирект на random).

Тесты
-----
Запуск тестов внутри контейнера:

```powershell
docker-compose exec web pytest -q
```

Конфигурация
-----------
Конфигурация по умолчанию: `config/config.yml`. Значения можно переопределить через ENV — приоритет ENV > YAML > дефолты.

Примеры ENV (см. `.env.example`):

```text
SECRET_KEY=changeme
DEBUG=True
MAX_QUOTES_PER_SOURCE=3
```

Production notes
----------------
Краткие рекомендации по деплою и настройке в `docs/PRODUCTION.md`.

Commit message для этого шага
----------------------------
`docs: add README with run and validation instructions`

Что дальше
----------
- Финальный прогон, очистка артефактов, production notes и CI. 
