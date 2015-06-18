# mappino RC1 #


## Deploy check list ##
* Перевірити чи Pillow збіраний з підтримкою jpeg/png шляхом загрузки jpeg фото в опис оголошення.


## Пам’ятка по керуванню сервером ##

### Дата/час у коректній часовій зоні ###
* Після налаштування wall-e слід виставити коректну часову зону для коректного відображення на фронті дат і часу.


### Біллінг ###
* Валюта біллінгу за замовчуванням — гривня. Під час інтернаціоналізації слід придумати механізм, який дозволив би в кожній країні користуватись власною валютою.

### Cache ###
* Всі темлейти на production кешуються по last-modified. Планувалось, що вони будуть кешуватись по etag з версією, але nginx починаючи з версії 1.3 вирізає etag з усіх запитів, які підлягають стисканню gzip. Тому зараз в хедер last-modified записується unix-timestamp, який одноразово генерується при першому запиті і зберігаєтсья в кеш редіса. При рестарті сервера даний ключ не скидається.  Для скидання кешу темплейтів слід видалити ключ "static_template_last_modified" з кеш-сервера redis.
