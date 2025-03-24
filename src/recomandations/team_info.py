import pandas as pd

def salary_cap(team):

    abb = pd.read_csv('~/course_proj_hse/data/Team Abbrev.csv')
    salary = pd.read_json('~/course_proj_hse/data/parsed/club_salary_parsed.json').T.reset_index().rename(
        columns={'index': 'Team'})

    cap = pd.merge(salary, abb, on='Team')

    salary_cap = cap.reset_index().rename(columns={'index': 'Rk'})
    salary_cap['Rk'] += 1


    team_cap = salary_cap[salary_cap['abbreviation'].str.lower() == team.lower()]
    rk = team_cap['Rk'].values[0]

    if rk in [1, 2]:
        final = salary_cap.head(5)
    elif rk in [29, 30]:
        final = salary_cap.tail(5)
    else:
        final = salary_cap.iloc[rk - 3:rk + 2]

    final = final[['Rk', 'Team', '2024-25']]

    final.to_csv("~/course_proj_hse/data/recs/Salary_Cap.csv", index=False)
    salary_cap.to_csv("~/course_proj_hse/data/recs/Salary.csv", index=False)

def status(team):
    if [team] < 178132000:
        return 'tax_free'
    elif df[team] > 188931000:
        return 'second_apron'
    else:
        return 'first_apron'


salary_cap(input())
