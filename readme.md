# Survey

## Создание виртуального окружения

```
python -m venv fabrique
```

## Активация виртуального окружения

### На Linux

```
source fabrique/bin/activate
```

### На Windows

```
fabrique\fabrique\Scripts\activate.bat
```

## Установка зависимостей

```
cd survey

python -m pip install -r requirements.txt
```

## Запуск приложения

1. Создание бд для проекта.

```
python manage.py migrate
```

2. Создание пользователя для управления опросами.

```
python manage.py createsuperuser
>> Username (leave blank to use 'fabrique'): staff [ENTE
>> Email address: [ENTER]
>> Password: *** [ENTER]
>> Password (again): *** [ENTER]
Superuser created successfully
```

3. Запуск сервера.

```
python manage.py runserver
```

## Получения списка api

### URL списка api

[Swagger ui](http://localhost:8000/swagger-ui)

### Авторизация

#### Получение токена

![api-token-auth](doc/api-token-auth.png)

#### Авторизация

В поле Value введите значение в виде

> `Token <token>`

![auth](doc/auth.png)

### Создание пользователя

`/api/v1/user/`

![create-user](doc/create-user.png)