from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'nope.accounts'

    def ready(self):
        # super(AccountsConfig, self).ready()
        # noinspection PyUnresolvedReferences
        import nope.accounts.signals  # noqa
