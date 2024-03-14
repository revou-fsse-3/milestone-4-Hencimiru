import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Perhatikan, path yang ditambahkan ke sys.path
# ini sesuai dengan struktur proyek Anda
sys.path.append(os.getcwd())

# Import model Anda di sini untuk mendapatkan akses ke MetaData
from models import base

# Ini adalah konfigurasi file Alembic
config = context.config

# Ini mengonfigurasi logger untuk penggunaan dalam
# debugging. Anda dapat mengabaikannya jika tidak diperlukan.
fileConfig(config.config_file_name)

# Ini adalah basis objek dari metadata Anda
# yang akan digunakan untuk autogenerate
target_metadata = base.metadata

# Konfigurasi koneksi database
config.set_main_option('sqlalchemy.url', 'mysql://root:12345678@localhost:3306/Banking-App')
# Misalnya, jika Anda ingin menggunakan autogenerate
# Anda perlu menyimpan metadata model Anda di
# dalam konteks seperti yang ditunjukkan di atas.

# Konteks ini digunakan ketika menjalankan perintah 'alembic revision'
# yang akan membuat skrip migrasi baru
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=target_metadata.schema,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Digunakan ketika menjalankan perintah 'alembic upgrade'
# yang akan menerapkan migrasi ke database
def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

# Perhatikan, untuk skenario penggunaan SQLite, Anda tidak perlu menutup
# koneksi setelah penggunaan, jadi Anda dapat menghapus blok try/finally
# dan hanya meninggalkan context.configure() di dalam blok with.
# Untuk penggunaan umum, Anda harus menghapus blok tersebut.

# Ketika menjalankan 'alembic upgrade' atau 'alembic downgrade', ini akan dipanggil.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
