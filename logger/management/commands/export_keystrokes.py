import csv
from django.core.management.base import BaseCommand
from logger.models import KeystrokeLog

class Command(BaseCommand):
    help = 'Export all keystroke logs to CSV'

    def handle(self, *args, **kwargs):
        with open('keystrokes_export.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'User', 'Key', 'Action', 'Rhythm',
                'Dwell Time', 'Flight Time', 'Up-Down Time',
                'Session Duration', 'Timestamp'
            ])

            for log in KeystrokeLog.objects.all():
                writer.writerow([
                    log.user.username if log.user else "Anonymous",
                    log.key, log.action, log.rhythm,
                    log.dwell_time, log.flight_time,
                    log.up_down_time, log.session_duration,
                    log.timestamp.isoformat()
                ])

        self.stdout.write(self.style.SUCCESS("✅ Keystroke data exported to keystrokes_export.csv"))

