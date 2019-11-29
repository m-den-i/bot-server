import asyncio
import concurrent.futures
import os
from unittest.mock import patch

import alembic.config
import asyncpg
import pytest
from databases import DatabaseURL

import settings
from database.db import DatabaseManager
from loop import event_loop, executor


@pytest.yield_fixture()
async def db_manager():
    db_conn_url = DatabaseURL(settings.DATABASE_CONNECTION_URL + '_test')
    database_manager = DatabaseManager(db_conn_url, force_rollback=True)
    _url = str(db_conn_url).split('/')
    _url_str = DatabaseURL('/'.join(_url[:-1] + ['template1']))

    try:
        conn = await asyncpg.connect(str(db_conn_url))
        print('DB exists')
    except asyncpg.InvalidCatalogNameError:
        print('DB doesn\'t exist. Creating new one.')
        # db_conn_url.components.path = 'template1'
        conn = await asyncpg.connect(str(_url_str))
        await conn.execute(
            F'create database {db_conn_url.database} '
            F'owner "{db_conn_url.username}"'
        )

    with patch.object(
            settings,
            'DATABASE_CONNECTION_URL',
            str(db_conn_url),
    ):
        alembicArgs = [
            '--raiseerr',
            '-c', 'alembic.ini',
            'upgrade', 'head',
        ]
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            executor,
            lambda: alembic.config.main(argv=alembicArgs)
        )
    await database_manager.connect()
    yield database_manager

    await database_manager.disconnect()
    await conn.close()
    conn = await asyncpg.connect(str(_url_str))
    if not os.environ.get('KEEP_TEST_DB'):
        try:
            await conn.execute(
                F'drop database {db_conn_url.database}'
            )
            print('DB deleted')
        except asyncpg.exceptions.ObjectInUseError:
            print('DB likely opened in your IDE. Delete manually')
    await conn.close()
