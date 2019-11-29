from command.base import CommandException
from database.models import User


def role_required(role):
    def dec(fn):
        def wrapped(self, *args, **kwargs):
            user = kwargs.get('user')

            if not isinstance(user, User):
                raise CommandException('Who are you?')

            if user.role != role:
                raise CommandException(
                    'You cannot run this command. '
                    'Role "{role}" is required'.format(role=User.ROLES[role])
                )

            return fn(self, *args, **kwargs)

        return wrapped

    return dec
