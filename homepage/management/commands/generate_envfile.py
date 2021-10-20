from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
	help = 'Creates .env file to be used with this project, Provided vars for grading purposes.'

	def handle(self, *args, **options):
		path = './config/.env'
		if not os.path.isfile(path):
			with open(path, 'w') as f:
				f.write(
					'''SECRET_KEY=django-insecure-)%074)l=t1=+#^#wc8!m+rf8*0^6&bdjb!^(a_e9cd@ks&861_
STATE_KEY=spotify_auth_state
CLIENT_ID=de48cb358c174f35976ac46f93640555
CLIENT_SECRET=7e5f4e8509ac42f4af3c6179bb408889
SCOPE="user-modify-playback-state user-read-playback-state streaming app-remote-control user-read-private user-read-email user-read-recently-played user-library-read playlist-read-private"
''')
				f.close()
			print('File Created Successfully')
		else:
			print('File Already Exists')
