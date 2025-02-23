import psycopg2
import os
import glob
import json
from dotenv import load_dotenv

HEADS = ['Name', 'url', 'rank', 'Age', 'Team', 'Pos', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'Awards']

def find_file(filename, search_path='.'):
    files = glob.glob(f'{search_path}/**/{filename}', recursive=True)
    return files[0] if files else None


def db_connect():
    load_dotenv()
    try:
        db = psycopg2.connect(dbname=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'), host='localhost')
        return db
    except:
        print('Can`t establish connection to database')

def player_advanced(db, cursor):
    cursor.execute("""DROP TABLE player_advanced""")
    db.commit()
    try:
        cursor.execute("""CREATE TABLE player_advanced ("Name" varchar, "Url" varchar, "Rank" integer, "Age" integer, "Team" varchar, "Pos" varchar, "G" integer, "GS" integer, "MP" integer, "PER" REAL, "TS%" REAL, "3PAr" REAL, "FTr" REAL, "ORB%" REAL, "DRB%" REAL, "TRB%" REAL, "AST%" REAL, "STL%" REAL, "BLK%" REAL, "TOV%" REAL, "USG%" REAL, "OWS" REAL, "DWS" REAL, "WS" REAL, "WS/48" REAL, "OBPM" REAL, "DBPM" REAL, "BPM" REAL, "VORP" REAL, "Awards" varchar)""")
        db.commit()
    except KeyError as e:
        print('I can`t create this table')
        print(e)

    with open("parsing/parsed/player_advanced.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for player in data.items():
        player_name = player[0]
        cursor.execute("""INSERT INTO player_advanced ("Name") VALUES (%s)""", [player_name])
        db.commit()

        query = """UPDATE player_advanced 
                SET "Url" = %s, "Rank" = %s, "Age" = %s, "Team" = %s, "Pos" = %s, "G" = %s, "GS" = %s, "MP" = %s, "PER" = %s, "TS%%" = %s, "3PAr" = %s, "FTr" = %s, "ORB%%" = %s, "DRB%%" = %s, "TRB%%" = %s, "AST%%" = %s, "STL%%" = %s, "BLK%%" = %s, "TOV%%" = %s, "USG%%" = %s, "OWS" = %s, "DWS" = %s, "WS" = %s, "WS/48" = %s, "OBPM" = %s, "DBPM" = %s, "BPM" = %s, "VORP" = %s, "Awards" = %s 
                WHERE "Name" = %s"""
        values = [None if v == '' else v for v in [*list(player[1].values()), player_name]]

        cursor.execute(query, values)
        db.commit()

def teams(db, cursor):
    cursor.execute("""DROP TABLE eastern_conference""")
    db.commit()
    cursor.execute("""DROP TABLE western_conference""")
    db.commit()

    try:
        cursor.execute("""CREATE TABLE eastern_conference ("Name" VARCHAR, "Url" VARCHAR, "Wins" INTEGER, "Losses" INTEGER, "Win/loss" REAL, "gb" REAL, "ps/g" REAL, "pa/g" REAL, "srs" REAL, "division" VARCHAR)""")
        db.commit()
    except KeyError as e:
        print('I can`t create this table')
        print(e)

    with open("parsing/parsed/eastern_standings.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for team in data.items():
        team_name = team[0]
        cursor.execute("""INSERT INTO eastern_conference ("Name") VALUES (%s)""", [team_name])
        db.commit()

        query = """UPDATE eastern_conference 
                SET "Url" = %s, "Wins" = %s, "Losses" = %s, "Win/loss" = %s, "gb" = %s, "ps/g" = %s, "pa/g" = %s, "srs" = %s, "division" = %s
                WHERE "Name" = %s"""
        values = [None if v == '' else v for v in [*list(team[1].values()), team_name]]

        cursor.execute(query, values)
        db.commit()

    try:
        cursor.execute("""CREATE TABLE western_conference ("Name" VARCHAR, "Url" VARCHAR, "Wins" INTEGER, "Losses" INTEGER, "Win/loss" REAL, "gb" REAL, "ps/g" REAL, "pa/g" REAL, "srs" REAL, "division" VARCHAR)""")
        db.commit()
    except KeyError as e:
        print('I can`t create this table')
        print(e)

    with open("parsing/parsed/western_standings.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for team in data.items():
        team_name = team[0]
        cursor.execute("""INSERT INTO western_conference ("Name") VALUES (%s)""", [team_name])
        db.commit()

        query = """UPDATE western_conference 
                SET "Url" = %s, "Wins" = %s, "Losses" = %s, "Win/loss" = %s, "gb" = %s, "ps/g" = %s, "pa/g" = %s, "srs" = %s, "division" = %s
                WHERE "Name" = %s"""
        values = [None if v == '' else v for v in [*list(team[1].values()), team_name]]

        cursor.execute(query, values)
        db.commit()
    

def db_fill():
    db: psycopg2.extensions.connection = db_connect()
    cursor  = db.cursor()

    player_advanced(db, cursor)
    teams(db, cursor)
    

        
if __name__ == '__main__':
    db_fill()