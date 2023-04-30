## Миграции
Все новые models.py нужно импортировать в env.py

### Создать ревизии:

`alembic revision --autogenerate -m 'ТЕКСТ ОПИСЫВАЮЩИЙ РЕВИЗИЮ'`

### Применить ревизию:

`alembic upgrade ХЭШ РЕВИЗИИ`

### Откатиться до ревизии:

`alembic downgrade ХЭШ РЕВИЗИИ`
