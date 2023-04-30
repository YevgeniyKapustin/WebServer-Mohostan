## Миграции
Все новые models.py нужно импортировать в env.py


### Создать ревизию:

`alembic revision --autogenerate -m 'ТЕКСТ ОПИСЫВАЮЩИЙ РЕВИЗИЮ'`

### Применить последнюю ревизию:

`alembic upgrade head`

### Применить ревизию:

`alembic upgrade ХЭШ РЕВИЗИИ`

### Откатиться до ревизии:

`alembic downgrade ХЭШ РЕВИЗИИ`
