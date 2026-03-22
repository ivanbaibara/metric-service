# Metric-Service

## 🎯 Суть проекта
Проект создан для накопления данных с iot датчиков, хранящихся в формате чисел с плавающей точкой (температура, влажность, давление и тому подобное).
В архитектуру заложена возможность в будущем записывать другие типы данных, на данный момент только float. 

Предусмотрена иерархия пользователей:
admin, user, spectator. Класс admin имеет отличительную возможность от класса user - добавление, удаление, просмотра информации о других пользователей.
Просмотр и управление данными других пользователей из класса admin - не возможен. Как и класс admin, класс user имеет возможность создавать метрики, 
изменять параметры (название, время хранения истории), добавлять данные и просматривать их. Так же реализована возможность добавлять к своим 
метрикам доступ других пользователей, при этом пользователь может быть только класса spectator. 

Класс spectator предназначен только для 
наблюдения за данными и не может ничего поменять в настройках метрик, только информацию о себе (пока что только пароль).

Описание полей сущности User:
- id: идентификатор пользователя
- role: класс пользователя, 0 - admin, 1 - user, 2 - spectator
- login: уникальное имя пользователя
- password: пароль пользователя

Описание полей сущности Metric:
- id: идентификатор метрики
- name: название метрики (может быть любым, метрики различаются только по id)
- type: тип данных метрики (пока что поддерживается только float) в таблице хранится как 3 символа, для float - flt
- duration: время хранения истории метрики в днях (пока не реализовано)

Так же существуют другие служебные таблицы. Ниже можно посмотреть описание методов API и название скриптов для их тестов.
Проект в разработке, поэтому запускается без внешнего wsgi, через встроенный сервер в flask.

## 🚀 Быстрый старт (uv)
Если у вас есть современный менеджер пакетов uv, рекомендуется поставить через него.

Копирование проекта:
```commandline
git clone https://github.com/ivanbaibara/metric-service
cd metric-service
```

Установка зависимостей:
```commandline
uv sync
```

Запуск проекта:
```commandline
uv run run.py
```

## 📦 Установка (через pip)
Если вы не хотите ставить uv, можно поставить через pip.

Копирование проекта:
```commandline
git clone https://github.com/ivanbaibara/metric-service
cd metric-service
```

Создание виртуального окружения (venv):
```commandline
python3 -m venv .venv
```

Активация venv:
```commandline
source .venv/bin/activate
```

Обновление pip и установка зависимостей:
```commandline
pip install --upgrade pip
pip install -r requirements.txt
```

Запуск сервиса:
```commandline
python run.py
```

Деактивация venv:
```commandline
deactivate
```

## 🏁 С чего начать

Для работы со скриптами требуется перейти в директорию bash (сделать в другом окне терминала, поскольку процесс сервиса привязан к окну терминала):
```commandline
cd bash
```

### 🔐 Авторизация
При первом запуске в базе данных существует только один пользователь класса admin, с логином и паролем admin.
На примере этого пользователя осуществим авторизацию в сервис (первый параметр - login, второй - password):
```commandline
auth/login.sh admin admin
```

Выход из сервиса:
```commandline
auth/logout.sh
```

### 👤 Управление пользователями
Желательно поменять пароль пользователя admin. Пароль меняется для пользователя, вошедшего в систему:
```commandline
users/update.sh new_pass
```
После замены пароля требуется войти еще раз с новым паролем.

Так же можно посмотреть информацию о себе:
```commandline
users/sels.sh
```

Остальные методы доступны только для пользователей класса admin.

Добавим по одному классу пользователей (что означают параметры - смотреть ниже раздел Методы API):
```commandline
users/add.sh 1 alice simple_pass
users/add.sh 2 maks simple_pass
```

Посмотрим, какие пользователи теперь есть в системе:
```commandline
users/all.sh
```

### 🏗 Добавление метрик 
Выйдем из системы (см. выше) и авторизуемся под пользователем alice:
```commandline
auth/login.sh alice simple_pass
```

Добавим пару метрик:
```commandline
metrics/add.sh temp_1 flt 31
metrics/add.sh temp_2 flt 31
```

Посмотрим, какие id метрик у нас есть:
```commandline
metrics/all.sh
```

Добавим разрешение на просмотр для одной из метрик пользователю maks:
```commandline
metrics/permissions/add.sh 1 maks
```

### 📊 Управление записями

Добавим пару записей в метрики по их id (первый параметр - id, второй - значение float):
```commandline
data/add.sh 1 10.2
data/add.sh 2 10.2
```
При желании можно добавить еще несколько с другими значениями.

Посмотрим, какие данные у нас в каждой метрике:
```commandline
data/get.sh 1
data/get.sh 2
```

Так же предлагается выйти и зайти под пользователем maks, чтобы посмотреть доступность данных.
Из минималистичных соображений тут описаны только некоторые методы, остальные смотреть ниже в таблице.



## 📜 Методы API 
В папке bash находятся bash-скрипты для тестирования и 
наглядного понимания работы эндпоинтов.

<details>
<summary>Нажми, чтобы увидеть таблицу методов</summary>

| Скрипт                        | Эндпоинт                          | Принимаемые параметры           | Уровень доступа | Описание работы                                                                                                                             |
|:------------------------------|:----------------------------------|:--------------------------------|:----------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| auth/login.sh                 | `POST /api/login`                 | `<login> <password>`            | all             | Авторизация через логин и пароль                                                                                                            |
| auth/logout.sh                | `POST /api/logout`                |                                 | all             | Выход из системы                                                                                                                            |
| data/add.sh                   | `POST /api/data`                  | `<metric_id> <value>`           | admin, user     | Запись значения метрики c metric_id и значением value                                                                                       |
| data/get.sh                   | `GET /api/data`                   | `<metric_id>`                   | all             | Получения всех значений метрики с metric_id                                                                                                 |
| data/last.sh                  | `GET /api/data/last`              | `<metric_id>`                   | all             | Получение последнего значения метрики с metric_id                                                                                           |
| metrics/add.sh                | `POST /api/metrics`               | `<name> <type> <duration>`      | admin, user     | Добавлении метрики с именем, типом данных и длительностью хранения истории (последние два параметра пока в разработке, но требуют указания) |
| metrics/all.sh                | `GET /api/metrics/all`            |                                 | all             | Получение всех доступных metric_id                                                                                                          | 
| metrics/delete.sh             | `DELETE /api/metrics`             | `<metric_id>`                   | admin, user     | Удаление метрики с metric_id                                                                                                                |
| metrics/one.sh                | `GET /api/metrics`                | `<metric_id>`                   | admin, user     | Получение информации о метрике с metric_id                                                                                                  | 
| metrics/update.sh             | `PATCH /api/metrics`              | `<metric_id> <name> <duration>` | admin, user     | Обновление имени и времени жизни данных для метрики с metric_id                                                                             |
| metrics/permissions/add.sh    | `POST /api/metrics/permissions`   | `<metric_id> <login>`           | admin, user     | Добавление владельца с login для метрики с metric_id (добавляемый владелец должен быть spectator)                                           | 
| metrics/permissions/all.sh    | `GET /api/metrics/permissions`    | `<metric_id>`                   | admin, user     | Просмотр всех владельцев метрики с metric_id                                                                                                |
| metrics/permissions/delete.sh | `DELETE /api/metrics/permissions` | `<metric_id> <login>`           | admin, user     | Удаление владельца с login для метрики с metric_id                                                                                          |
| users/add.sh                  | `POST /api/users`                 | `<role> <login> <password>`     | admin           | Добавлние нового пользователя с role, login, password                                                                                       |
| users/all.sh                  | `GET /api/users/all`              |                                 | admin           | Просмотр всех пользователей в системе                                                                                                       |
| users/delete.sh               | `DELETE /api/users`               | `<user_id>`                     | admin           | Удаление пользователя с user_id                                                                                                             |
| users/one.sh                  | `GET /api/users`                  | `<user_id>`                     | admin           | Просмотр пользователя с user_id                                                                                                             |
| users/update.sh               | `PATCH /api/users`                | `<password>`                    | all             | Обновление своего пароля. При обновлении все сессии сбросятся                                                                               |

</details>