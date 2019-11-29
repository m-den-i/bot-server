from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from loop import event_loop
from settings import DATABASE_CONNECTION_URL

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_CONNECTION_URL),
}
executors = {
    'default': AsyncIOExecutor(),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3,
}


scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
    event_loop=event_loop,
)
