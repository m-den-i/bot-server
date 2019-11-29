from unittest.mock import patch
from aiohttp import web

import settings


def test_app_conf():
    with patch.object(web, 'run_app') as fake_run_app:
        from main import app
        fake_run_app.assert_called_with(
            app,
            host=settings.APP['host'],
            port=settings.APP['port'],
        )
