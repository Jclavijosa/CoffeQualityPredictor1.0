# alembic/env.py

import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.base import Base  # Importa la base de tus modelos
from app.core.config import settings  # Importa las configuraciones

config = context.config
fileConfig(config.config_file_name)

# Configura la URL de la base de datos desde settings
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
