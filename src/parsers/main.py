from club_salary_parse import club_salary_parse
from player_salary_parse import player_salary_parse
from season_summary import season_summary
from player_advanced import player_advanced


# comment which is NOT needed to be parsed
def main():
    club_salary_parse()
    player_salary_parse()
    season_summary()
    player_advanced()

if __name__ == '__main__':
    main()
