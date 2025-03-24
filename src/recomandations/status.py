import pandas as pd
df = pd.read_csv("~/course_proj_hse/data/recs/Salary.csv")

def status(team):
    if df[Team]['2024-2025'] < 178132000:
        return 'tax_free'
    elif df[team]['2024-2025'] > 188931000:
        return 'second_apron'
    else:
        return 'first_apron'


status('Phoenix Suns')