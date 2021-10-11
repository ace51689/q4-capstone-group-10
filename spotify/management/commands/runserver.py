from django.core.management.base import BaseCommand
from os import system as run


class Command(BaseCommand):
	def handle(self, *args, **options):
		run('python manage.py runsslserver')
		return '\n'
