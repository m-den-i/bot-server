from datetime import date

from loop import event_loop
from .scheduler import scheduler

DATE_TASK = 0
CRON_TASK = 1


class APTask:
    def __init__(self, task_type, fn):
        self.task_type = task_type
        self.fn = fn
        self.job = None

    async def start(self, run_datetime=None, cron_rule=None,
                    args=(), kwargs=None,
                    *targs, **tkwargs):
        if self.task_type == DATE_TASK:
            if not isinstance(run_datetime, date):
                raise Exception(
                    'run_datetime param is not date/datetime instance'
                )
            self.job = await event_loop.run_in_executor(
                None,
                lambda: scheduler.add_job(
                    self.fn, 'date',
                    args=args,
                    kwargs=kwargs or {},
                    run_date=run_datetime,
                    *targs, **tkwargs
                )
            )
        elif self.task_type == CRON_TASK:
            self.job = await event_loop.run_in_executor(
                None,
                lambda: scheduler.add_job(
                    self.fn, 'cron',
                    args=args,
                    kwargs=kwargs,
                    *targs,
                    **dict(tkwargs, **cron_rule)
                )
            )
        else:
            raise Exception('Unknown type of task')


def bg_task(task_type):
    def dec(fn):
        fn.task = APTask(task_type, fn)
        return fn

    return dec
