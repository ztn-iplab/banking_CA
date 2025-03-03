from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Run the keylogger in the background'

    def handle(self, *args, **kwargs):
        # Adjust the command based on how you want to run the keylogger
        subprocess.Popen(['python', 'path/to/your/keylogger/keylogger.py'])
        self.stdout.write(self.style.SUCCESS('Keylogger is running in the background'))
