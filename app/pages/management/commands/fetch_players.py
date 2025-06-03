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
                    image_url=row[3],
                    age=row[4],
                    team=row[5],
                    position=row[6],
                    g = row[7],
                    gs = row[8],
                    mp = row[9],
                    per = row[10],
                    ts = row[11],
                    par = row[12],
                    ftr = row[13],
                    orb = row[14],
                    drb = row[15],
                    trb = row[16],
                    ast = row[17],
                    stl = row[18],
                    blk = row[19],
                    tov = row[20],
                    usg = row[21],
                    ows = row[22],
                    dws = row[23],
                    ws = row[24],
                    ws48 = row[25],
                    obpm = row[26],
                    dbpm = row[27],
                    bpm = row[28],
                    vorp = row[29],
                    awards = row[30],
                    pos = row[31],
                    neu = row[32],
                    neg = row[33],
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
