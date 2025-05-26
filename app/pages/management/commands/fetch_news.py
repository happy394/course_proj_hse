from django.core.management.base import BaseCommand
from pages.models import Player, PlayerNews
import psycopg2
from django.utils import timezone
from django.conf import settings
from datetime import datetime


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

            news_entries = []
            for row in rows:
                player_name, timestamp, source, text = row
                player = Player.objects.filter(name=player_name).first()

                if player:
                    news_entries.append(
                        PlayerNews(
                            player=player,
                            timestamp = timezone.make_aware(datetime.fromtimestamp(int(timestamp))),
                            source=source,
                            text=text
                        )
                    )

            # Delete existing news and insert new ones
            PlayerNews.objects.all().delete()
            PlayerNews.objects.bulk_create(news_entries, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(news_entries)} news articles!"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
