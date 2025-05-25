import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.bottec_bot.config import config as app_config
from app.bottec_bot.db.session import Base
from app.bottec_bot.db import models

# Alembic Config object
config = context.config

# Логирование
fileConfig(config.config_file_name)

# Установка строки подключения из переменных окружения
DATABASE_URL = (
    f'postgresql+asyncpg://{app_config.POSTGRES_USER}:{app_config.POSTGRES_PASSWORD}'
    f'@{app_config.POSTGRES_HOST}:{app_config.POSTGRES_PORT}/{app_config.POSTGRES_DB}'
)
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Метадата для Alembic
target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций в offline-режиме."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в online-режиме (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
