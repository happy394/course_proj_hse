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

            cur.execute("""SELECT * FROM player_advanced WHERE "Name" <> 'League Average' """)
            rows = cur.fetchall()

            players = [
                Player(
                    name=row[0],
                    rank=row[2],
                    age=row[3],
                    team=row[4],
                    position=row[5],
                    g = row[6],
                    gs = row[7],
                    mp = row[8],
                    per = row[9],
                    ts = row[10],
                    par = row[11],
                    ftr = row[12],
                    orb = row[13],
                    drb = row[14],
                    trb = row[15],
                    ast = row[16],
                    stl = row[17],
                    blk = row[18],
                    tov = row[19],
                    usg = row[20],
                    ows = row[21],
                    dws = row[22],
                    ws = row[23],
                    ws48 = row[24],
                    obpm = row[25],
                    dbpm = row[26],
                    bpm = row[27],
                    vorp = row[28],
                    awards = row[29],
                ) for row in rows
            ]

            # check = input('Type y or n to empty the table\n')
            # if check == 'y':
            #     Player.objects.all().delete()
            # else:
            #     pass
            Player.objects.all().delete()

            Player.objects.bulk_create(players, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f"Successfully updated {len(players)} players data!"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))