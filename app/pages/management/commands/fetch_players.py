from django.core.management.base import BaseCommand
from pages.models import Player
import psycopg2
from django.conf import settings

class Command(BaseCommand):
    help = "Fetch latest employee data from PostgreSQL and update the Django database"

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

            cur.execute("""SELECT "Rank", "Name", "Team", "Pos" FROM player_advanced WHERE "Name" <> 'League Average' """)
            rows = cur.fetchall()

            players = [
                Player(
                    rank=row[0],
                    name=row[1],
                    team=row[2],
                    position=row[3]
                ) for row in rows
            ]

            check = input('Type y or n to empty the table\n')
            if check == 'y':
                Player.objects.all().delete()
            else:
                pass

            Player.objects.bulk_create(players, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f"Successfully updated {len(players)} players data!"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))