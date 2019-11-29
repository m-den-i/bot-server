from databases import Database


class DatabaseManager(object):

    def __init__(self, db_url, **kwargs):
        self.db = Database(url=db_url, **kwargs)

    async def connect(self, *args):
        await self.db.connect()

    async def disconnect(self, *args):
        await self.db.disconnect()
