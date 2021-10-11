from sslserver.management.commands import runsslserver


class Command(runsslserver.Command):
	def handle(self, *args, **options):
		super(Command, self).handle(self, *args, **options)
		return '\n'
