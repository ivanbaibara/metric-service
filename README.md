# Metric-Service

## 🎯 Суть проекта
Тут будет описание

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

## 📦 Установка (Через pip)
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