from django.core.management.base import BaseCommand
from pages.models import Team_east, Team_west
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

            cur.execute("""SELECT "Name" FROM eastern_conference""")
            rows_east = cur.fetchall()

            cur.execute("""SELECT "Name" FROM western_conference""")
            rows_west = cur.fetchall()

            teams_east = [
                Team_east(
                    name=row[0],
                ) for row in rows_east
            ]

            teams_west = [
                Team_west(
                    name=row[0],
                ) for row in rows_west
            ]

            check = input('Type y or n to empty the table\n')
            if check == 'y':
                Team_east.objects.all().delete()
                Team_west.objects.all().delete()
            else:
                pass

            Team_east.objects.bulk_create(teams_east, ignore_conflicts=True)
            Team_west.objects.bulk_create(teams_west, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f"Successfully updated {len(teams_east)+len(teams_west)} teams data!"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))