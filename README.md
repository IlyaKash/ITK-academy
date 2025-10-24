### Запуск приложения через Docker Compose

1. Перейти в корень проекта:
```cd ITK-academy```

2. Создать файл .env в корне проекта и скопировать туда данные из .enx.example

3. Поднять контейнеры и собрать контейнеры:
```docker-compose up -d```

4. Проверить запуск контейнеров:
```docker ps```
Должны присутствовать:
test_db — база данных Postgres
test_api — FastAPI 

Доступ к приложению: [http://localhost:8000](http://localhost:8000)

5. Остановка и удаление контейнеров
```docker-compose down -v```
