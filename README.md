# DjangoBlog v.1.0
Блог написан на Django. Читать статьи (посты) могут все без регистрации. Создавать, редактировать и удалять статьи могут только зарегистрированные пользователи. 
Создавать и редактировать категории могут только администраторы и персонал сайта.
Реализована обратная связь с администратором сайта через e-mail сообщения. Возможно отправить запрос добавить категорию, сообщить об ошибке или пожелания по улучшению сайта, прочее.
Также через e-mail сообщения реализовано восстановление пароля пользователя. Работа с сайтом возможна через REST API, его подробное описание приведено ниже.

При написании приложения использованы следующие основные пакеты, фреймворки и технологии: \
[Django](https://pypi.org/project/Django/); \
[Django REST framework](https://www.django-rest-framework.org); \
[Django Debug Toolbar](https://pypi.org/project/django-debug-toolbar/); \
[Django Simple Captcha](https://pypi.org/project/django-simple-captcha/); \
[Django CKEditor](https://pypi.org/project/django-ckeditor/); \
[Bootstrap](https://bootstrap-4.ru/).

Полный список можно посмотреть в фале 'requirements.txt'.

База данных [SQLite3](https://www.sqlite.org/index.html).

### Описание Models
##### Приложение "blog"
> Category - категории для группировки статей.
>> id - уникальный идентификатор, присваивается автоматически.\
>> title - название категории.\
>> slug - slag для формирования url-адреса, формируется автоматически на основании поля title.

> Post - статьи (посты).
>> id - уникальный идентификатор, присваивается автоматически.\
>> user - автор статьи, связь один со многими с моделью django.contrib.auth.models.User.\
>> cat - категория, связь один со многими с моделью Category.\
>> title - название статьи.\
>> slug - slag для формирования url-адреса, формируется автоматически на основании поля title.\
>> body - текст статьи. \
>> time_created - дата создания статьи, присваивается автоматически. \
>> likes - лайки, связь многие со многими с моделью django.contrib.auth.models.User.

##### Приложение "members"
> Profile - дополнительная информация о пользователе.
>> id - уникальный идентификатор, присваивается автоматически.\
>> user - пользователь, связь один с одним с моделью django.contrib.auth.models.User.\
>> slug - slag для формирования url-адреса, формируется автоматически на основании поля username модели User с добавлением суффикса '-profile'.\
>> image - аватар пользователя.\
>> bio - информация пользователя о себе.\
>> ya_url - ссылка на профиль в Яндекс.\
>> vk_url - ссылка на профиль в ВКонтакте.\
>> ok_url - ссылка на профиль в Одноклассники.\
>> git_url - ссылка на профиль в Git.\
>> website_url - ссылка на website пользователя.

## Описание REST API
Реализовано REST API для чтения и добавления категорий (читать могут все, добавлять только персонал сайта), чтение, добавление, 
обновление и удаление статей (читать могут все, добавлять только авторизованные пользователи, править только авторы статьи или персонал сайта).
Используется базовая аутентификация, имя пользователя и пароль в заголовке запроса.

### Категории
При добавлении категории достаточно передать только ее название (поле title), url-адрес будет сформирован автоматически (поле slug).
Также необходимо передать логин и пароль пользователя, который имеет статус персонала (is_staff).

Реализованы следующие методы: 

##### GET `http://127.0.0.1:8000/api/categories/` - получить все категории
Ответ `[{"id":1,"slug":"raznoe","title":"Разное"}, ...]` \
Статус 200 Ok

##### POST `http://127.0.0.1:8000/api/categories/` body `{"title":"Разное"}` - добавить категорию
Ответ `{"id":1,"slug":"raznoe","title":"Разное"}` \
Статусы:
- 201 Created
- 403 Forbidden {"detail": "Учетные данные не были предоставлены."}
- 400 Bad Request {'info': 'Только администраторы сайта могут добавлять статьи.'}
- 400 Bad RequestT {"title": ["Это поле обязательно для заполнения."]}
- 400 Bad Request {'error': 'Неправильный запрос.'}

### Статьи
Для добавления статьи необходимо передать зарегистрированного пользователя, id категории (cat), название (title) и текст статьи (body), остальные поля будут сформирован автоматически.
Для редактирования или удаления статьи необходимо передать автора этой статьи.

Реализованы следующие методы: 

##### GET `http://127.0.0.1:8000/api/posts/` - получить все статьи
Ответ `[
    {
        "id": 1,
        "user": "admin",
        "cat": 1,
        "title": "Первая статья",
        "slug": "pervaya-statya",
        "body": "Текст первой статьи",
        "time_created": "2023-02-06T19:29:16.718989Z",
        "likes": []
    }, ...]` \
Статус 200 Ok

##### GET `http://127.0.0.1:8000/api/posts/<slug>` - получить одну статью
где `<slug>` - значение поля "slug" статьи, для получения указанного ниже ответа запрос должен быть `http://127.0.0.1:8000/api/posts/pervaya-statya` \
Ответ `{
            "id": 1,
            "user": "admin",
            "cat": 1,
            "title": "Первая статья",
            "slug": "pervaya-statya",
            "body": "Текст статьи",
            "time_created": "2023-02-07T18:30:54.110166Z",
            "likes": []
        }`
Статус 200 Ok

##### POST `http://127.0.0.1:8000/api/posts/` body `{"cat": 1,"title": "Первая статья","body": "Текст первой статьи"}` - добавить статью
Ответ `{
        "id": 1,
        "user": "admin",
        "cat": 1,
        "title": "Первая статья",
        "slug": "pervaya-statya",
        "body": "Текст первой статьи",
        "time_created": "2023-02-06T19:29:16.718989Z",
        "likes": []
    }` \
Статусы:
- 201 Created
- 403 Forbidden {"detail": "Учетные данные не были предоставлены."}
- 400 Bad RequestT {"cat":["Это поле обязательно для заполнения."],"title":["Это поле обязательно для заполнения."]}



## Проверка API с использованием [curl](https://curl.se/docs/manual.html)
### Категории
Создаем категорию (при необходимости исправьте данные пользователя "-u admin:You_Admin_password!") \
Запрос `curl -d '{"title":"Разное"}' -H "Content-Type: application/json" -u admin:You_Admin_password! -X POST http://127.0.0.1:8000/api/categories/` \
Ответ  `{"id":1,"slug":"raznoe","title":"Разное"}`

Читаем категории \
Запрос `curl -X GET http://127.0.0.1:8000/api/categories/` \
Ответ  `[{"id":1,"slug":"raznoe","title":"Разное"}, ...]`

### Статьи
Создаем статью (при необходимости исправьте данные пользователя "-u admin:You_Admin_password!")\
Запрос `curl -d '{"cat":1,"title":"Первая статья","body":"Текст статьи"}' -H "Content-Type: application/json" -u admin:You_Admin_password! -X POST http://127.0.0.1:8000/api/posts/` \
Ответ `{"id":1,"user":"admin","cat":1,"title":"Первая статья","slug":"pervaya-statya","body":"Текст статьи","time_created":"2023-02-07T18:30:54.110166Z","likes":[]}`

Читаем статьи \
Запрос `curl -X GET http://127.0.0.1:8000/api/posts/` \
Ответ `[{"id":1,"user":"admin","cat":1,"title":"Первая статья","slug":"pervaya-statya","body":"Текст статьи","time_created":"2023-02-07T18:30:54.110166Z","likes":[]}, ...]`

## Установка и запуск

#### Локально на Вашем устройстве (используя отладочный сервер)
Приложение написано на [Python v.3.11](https://www.python.org). 
1. Скачайте DjangoBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Python](https://www.python.org), если он у Вас еще не установлен.
3. Установите необходимые для работы приложения модули. Для этого откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/DjangoBlog), выполните команду `pip3 install -r requirements.txt`. Если Вы пользователь Microsoft Windows, то вместо `pip3 install ...` следует использовать  `pip install -r requirements.txt`
4. Установите [переменную окружения](https://wiki.archlinux.org/title/Environment_variables_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)) `SECRET_KEY`, например выполнив в терминале `export SECRET_KEY="ваш_сложный_секретный_ключ_djang"`.
5. Для запуска приложения локально на Вашем устройстве перейдите в папку `website` (`cd website` или `dir website` для Windows) выполните команду `python3 manage.py runserver` (Для Microsoft Windows `python manage.py runserver`).
6. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:8000/
#### В контейнере Docker (используя отладочный сервер)
1. Скачайте FlaskBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Docker](https://www.docker.com/), если он у Вас еще не установлен.
3. Откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/DjangoBlog).
4. В Dockerfile установите Ваши значения переменных окружения `SECRET_KEY`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` и `DJANGO_SUPERUSER_USERNAME`.
5. Выполните сборку Docker образа (image) `docker build -t django_blog .`.
6. Запустите контейнер `docker run -p 8000:8000 -d django_blog`.
7. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:8000/

### Настройка приложения
Откройте файл `website/website/settings.py` \
`PAGINATE_BY_CONST = 25` - задает сколько постов будет отображаться на странице. \
`ALL_CATEGORIES = {'title': 'Все категории', 'slug': 'all-categories'}` - задает название для всех категорий, сейчас установлено "Все категории", можно поменять только его, slug менять необязательно. \
`EMAIL_THEME_CHOICES = ` - перечень тем для писем при обращении к администратору сайта.