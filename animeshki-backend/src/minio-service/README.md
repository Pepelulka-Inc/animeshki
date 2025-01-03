## Первоначальная настройка MinIO

При первом запуске `MinIO`, она создается пустой.
Однако для корректной работы `minio-service` перед
запуском приложения уже должен быть создан
пользователь и бакет для хранения файлов.
Если директория `/data` будет примонтирована к директории,
где уже хранится информация о пользователях и бакетах,
то ничего изначально создавать не надо.

Поэтому я решил добавить такую логику в запуск сервиса -
сервис можно запускать в нескольких режимах - с
инициализацией (то есть с первоначальным созданием 
пользователя и бакета) или без.

Для запуска с инициализацией необходимо перед запуском
контейнера выставить переменную окружения
`MINIO_SERVICE_INIT_MODE=1`

Независимо от режима запуска в .env файле необходимо
выставить следующие переменные окружения:

 - Указать логин и пароль для пользователя, который
будет создан в переменных `MINIO_SERVICE_USER_NAME` и
`MINIO_SERVICE_USER_PASSWORD`
 - Указать имя бакета, который будет использоваться в
переменной `MINIO_SERVICE_BUCKET_NAME`

А конкретно для запуска с инициализацией необходимо
выставить следующие переменные:
 - Указать имя и пароль для рута:
`MINIO_ROOT_USER` и `MINIO_ROOT_PASSWORD`
