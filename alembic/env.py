import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from src.shared_kernel.infrastructure.config import settings

project_root = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)
sys.path.insert(
    0,
    project_root,
)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)  # type:ignore

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from src.shared_kernel.infrastructure.config import Base, GUID_Type
from src.shared_kernel.infrastructure import models as SharedKernelModels
from src.identity_access_management.infrastructure import models as IAMModels


target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def process_revision_directives(context, revision, directives):
    """
    Prevents Alembic from generating type-change migrations for UUID
    columns when the backend is SQLite.
    This is necessary due to a SQLite limitation with autogenerate.
    """

    if context.dialect.name != "sqlite":
        return

    script = directives[0]
    if script.upgrade_ops is None:
        return

    for script in directives:
        if script.upgrade_ops is not None:
            new_upgrade_ops = []
            for op in script.upgrade_ops.ops:
                is_alter_uuid = (
                    op.__class__.__name__ == "ModifyTableOps"
                    and op.ops[0].__class__.__name__ == "AlterColumnOp"
                    and "UUID" in str(getattr(op.ops[0], "modify_type", ""))
                )
                if is_alter_uuid:
                    print(f"INFO: Ignorando operação de UPGRADE para UUID no SQLite.")
                    continue
                new_upgrade_ops.append(op)
            script.upgrade_ops.ops = new_upgrade_ops

        if script.downgrade_ops is not None:
            new_downgrade_ops = []
            for op in script.downgrade_ops.ops:
                is_alter_uuid = (
                    op.__class__.__name__ == "ModifyTableOps"
                    and op.ops[0].__class__.__name__ == "AlterColumnOp"
                    and "UUID" in str(getattr(op.ops[0], "existing_type", ""))
                )
                if is_alter_uuid:
                    print(f"INFO: Ignorando operação de DOWNGRADE para UUID no SQLite.")
                    continue
                new_downgrade_ops.append(op)
            script.downgrade_ops.ops = new_downgrade_ops


def render_item(type_, obj, autogen_context):
    """
    Renderiza o tipo GUID_Type customizado corretamente no ficheiro de migração,
    adicionando o import necessário.
    """
    # Verifica se é o nosso tipo customizado
    if type_ == "type" and isinstance(obj, GUID_Type):
        # Adiciona o import no topo do ficheiro de migração gerado
        autogen_context.imports.add(
            "from src.shared_kernel.infrastructure.config.custom_types import GUID_Type"
        )
        # Renderiza o tipo como "GUID_Type()"
        return "GUID_Type()"

    # Deixa o Alembic lidar com todos os outros tipos
    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
        render_as_batch=True,
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            render_as_batch=True,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
