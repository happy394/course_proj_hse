from django.core.management.base import BaseCommand
from pages.models import Player, PlayerNews
import psycopg2
from django.conf import settings
from datetime import datetime
from datetime import timezone as dt_timezone


class Command(BaseCommand):
    help = "Fetch latest player news from PostgreSQL and update the Django database"

    def handle(self, *args, **kwargs):
        try:
            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
            )
            cur = conn.cursor()
            cur.execute("""SELECT "Player", "Timestamp", "Source", "Text" FROM mentions""")
            rows = cur.fetchall()

            # Delete existing news and insert new ones
            PlayerNews.objects.all().delete()

            count = 0
            for player_name, timestamp, source, text in rows:
                player = Player.objects.filter(name=player_name).first()

                if player:
                    PlayerNews.objects.create(
                        player=player,
                        timestamp=datetime.fromtimestamp(timestamp, tz=dt_timezone.utc),
                        source=source,
                        text=text
                    )
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} news articles!"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
