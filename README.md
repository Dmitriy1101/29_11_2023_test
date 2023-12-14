# 29_11_2023_test
Это выполненое задание:
https://docs.google.com/document/d/1X8yV7jAZWZWhy3NG3m_Yi8lW4Bfa6ZNGDx95pHkE_qc/edit#heading=h.qn8kbnfz56hc

# Здравствуйте

## Все просто:
- Выполнено на Python 3.11
- Подготовка:
  - Вам понадобится регистрация на https://stripe.com/ 
  - Необходимо создать файл `.env` в `29_11_2023_test\test_project\` и в нем указать:
      ```
        SECRET_KEY=django-Секрет
        STRIPE_TEST_PKEY=pk_test_очень большой секрет от stripe
        STRIPE_TEST_SKEY=sk_test_очень большой секрет от stripe
        STRIPE_TEST_WEBHOOK=
        DEBUG=True
        success_url=http://127.0.0.1:8000/payment_successful
        return_url=http://127.0.0.1:8000/payment_cancelled
      ``` 
  - И не забываем про Docker
- Важно:
  - Для удобства тестирования в джанго модели Items мной настороена автоматическая регистрация товара на сайте stripe, но:
    - Так как в "жизни" данное решение без согласования мной с проектом не пошло бы в "жизнь", не ждите полного функционала.
    - При изменении экземпляра модели Items на сайте stripe будет создоваться новый товар!
  - `29_11_2023_test\dbdata\db` сюда будут сохранены даныые Postgres из контейнера
- Для работы:
  - Рабочая директория: `29_11_2023_test`
  - Начало с Docker: `docker-compose build` 
  - При необходимости создать миграции: `docker compose run --rm web-app sh -c "python manage.py makemigrations"` 
    - Возможно потребуется более явно: `docker compose run --rm web-app sh -c "python manage.py makemigrations stripe_api"`
  - Запускаем миграции: `docker compose run --rm web-app sh -c "python manage.py migrate"`
  - Для подключения к Admin панели незабываем про: `docker compose run --rm web-app sh -c "python manage.py createsuperuser"`
  - Запускаем контейнер: `docker-compose up`
- Для тестирования:
  - На административном сайте создаем тестовые товары.
  - Тестирование начинается отсюда: `http://127.0.0.1:8000/item/`
  - Тестовые данные для покупок: `https://stripe.com/docs/testing#cards`
  
#### Буду рад критике