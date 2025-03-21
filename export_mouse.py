import csv
from django.core.management.base import BaseCommand
from logger.models import MouseActionLog

class Command(BaseCommand):
    help = 'Export all mouse action logs to CSV'

    def handle(self, *args, **kwargs):
        with open('mouse_export.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'User', 'Action', 'Coordinates', 'Button',
                'Delta', 'Distance', 'Speed', 'Timestamp'
            ])

            for log in MouseActionLog.objects.all():
                writer.writerow([
                    log.user.username if log.user else "Anonymous",
                    log.action, log.coordinates, log.button,
                    log.delta, log.distance, log.speed,
                    log.timestamp.isoformat()
                ])

        self.stdout.write(self.style.SUCCESS("✅ Mouse data exported to mouse_export.csv"))

