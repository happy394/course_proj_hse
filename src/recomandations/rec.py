import pandas as pd

advanced = pd.read_json('~/course_proj_hse/data/parsed/player_advanced.json').T.reset_index().rename(columns={'index': 'Player'})
# Open the file containing salary information
salary = pd.read_json('~/course_proj_hse/data/parsed/player_salary_parsed.json').T.reset_index().rename(columns={'index': 'Player'})


# Merge the filtered advanced statistics and salary DataFrames based on Player names
# Drop the 'birth_year' column after merging
total = pd.merge(advanced, salary, on='Player', how='inner')
total = total[total['PER'] > 0]


# Filter the merged DataFrame based on the team name entered by the user


def real_sum(col: list, DataFrame):
    """
    Function to calculate a weighted sum based on column values.

    Args:
        col (list): List of column names to consider for calculation.
        DataFrame (DataFrame): Pandas DataFrame containing the data.

    Returns:
        int: Weighted sum of the specified columns.
    """
    k = 0
    # Determine the number of columns with non-zero values
    for name in col:
        if DataFrame[name] != 0:
            k += 1
        else:
            break

    # Define weights for each column
    summ = [0.3, 0.25, 0.2, 0.15, 0.1, 0.05]
    # Calculate the divisor for normalization
    div = sum(summ[:k])
    right_sum = 0
    num = 0
    # Calculate the weighted sum
    for name in col[:k]:
        right_sum += DataFrame[name] * summ[num] / div
        num += 1
    return int(right_sum)

def convert_int_to_dollar(n):
    """
    Function to convert integer values to dollar strings.

    Args:
        n (int): Integer value to be converted.

    Returns:
        str: Dollar string representation of the integer amount.
    """
    if isinstance(n, int):
        # Format the integer with commas and add a dollar sign
        return "${:,}".format(n)
    else:
        return "$0"  # Return $0 if input is not an integer

def getTeamResult(team):
    curTeam = total.loc[total['Team'].str.lower() == f'{team}'.lower()]

    # "Here begins the output of Table 1"

    # Sort the DataFrame by minutes played in descending order and select relevant columns
    mp_team = curTeam.sort_values(by='MP', ascending=False)[['Pos', 'Player', 'guaranteed']]

    # Avoid errors with the starting lineup (each Player must be from their respective position)
    squad = pd.DataFrame(columns=['Pos', 'Player', 'guaranteed'])
    pos = ['PG', 'SG', 'SF', 'PF', 'C']

    for i in pos:
        # Filter players by position
        curPos = (mp_team.loc[mp_team['Pos'] == f'{i}'])
        # Select the Player with the maximum time played for each position
        try:
            Player = curPos.loc[curPos['Pos'] == f'{i}'].iloc[0]
        except IndexError:
            continue  # If no Player found for a position, continue to the next position
        squad = squad._append(Player)  # Append the Player to the squad DataFrame

    # Get the indices of players in the starting lineup
    selected_players_index = squad.index.tolist()

    # Remove players from the starting lineup and display all remaining players sorted by time played
    curTeam_updated = mp_team.drop(index=selected_players_index)
    squad = squad._append(curTeam_updated)
    squad['guaranteed'] = squad['guaranteed'].apply(convert_int_to_dollar)
    print(squad)
    squad.to_csv("~/course_proj_hse/data/recs/Squad.csv")



    squa = pd.DataFrame(columns=['Pos', 'Player', 'guaranteed'])
    per_team = curTeam.sort_values(by='PER', ascending=False)[['Pos', 'Player', 'guaranteed']]
    for i in pos:
        # Filter players by position
        curPos = (per_team.loc[per_team['Pos'] == f'{i}'])
        # Select the Player with the maximum time played for each position
        try:
            Player = curPos.loc[curPos['Pos'] == f'{i}'].iloc[0]
        except IndexError:
            continue
        squa = squa._append(Player)  # Append the Player to the squad DataFrame
        per_team_players_index = squa.index.tolist()

    further = set(per_team_players_index + selected_players_index)


    for i in further:
        if i in curTeam.index:
            curTeam = curTeam.drop(index=i)

    columns = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']


    # Calculate total salary using real_sum function for each row
    curTeam['Total Salary'] = curTeam.apply(lambda row: real_sum(columns, row), axis=1)

    # Select necessary columns for final DataFrame
    final_df = curTeam[['Player', 'Pos', 'MP', 'Age', 'PER', 'Total Salary']]

    # Calculate a metric combining salary and performance (wrong formula)
    final_df['price/quality'] = final_df.apply(lambda row: int(row['Total Salary']/row['PER']), axis=1)
    # The formula should be updated, as noted.

    # Sort the DataFrame by the calculated metric
    final = final_df.sort_values(by='price/quality', ascending=False).head()


    to_replace = final[['Pos', 'Total Salary']]
    final['Total Salary'] = final['Total Salary'].apply(convert_int_to_dollar)

    final = final[['Player', 'Pos']]
    final.to_csv("~/course_proj_hse/data/recs/Kick.csv")

    qwerty = total[['Player', 'Team', 'Pos', 'PER', '2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']]

    columns = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']


    qwerty = qwerty[qwerty['PER'] != 0]
    qwerty = qwerty[qwerty['Team'] != team]

    # Calculate total salary using real_sum function for each row
    qwerty['Total Salary'] = qwerty.apply(lambda row: real_sum(columns, row), axis=1)
    qwerty = qwerty[qwerty['Total Salary'] != 0]
    # Calculate a metric combining salary and performance (wrong formula)
    qwerty['price/quality'] = qwerty.apply(lambda row: int(row['Total Salary'] / row['PER']), axis=1)

    qwerty = qwerty.sort_values(by='price/quality', ascending=True)

    # Create a DataFrame to store the selected players
    Output = pd.DataFrame(columns=qwerty.columns)

    # Iterate over to_replace DataFrame and find matching players in qwerty
    for index, row in to_replace.iterrows():
        Pos = row['Pos']
        salary = row['Total Salary']
        i = 0
        while i < len(qwerty):
            best_player = qwerty[qwerty['Pos'] == Pos].iloc[i]
            if 100 - (best_player['Total Salary'] / salary * 100) <= abs(5):
                Output = Output._append(best_player)
                break
            i += 1

    Output = Output[['Player', 'Team', 'Pos']]

    Output.to_csv("~/course_proj_hse/data/recs/Newcomers.csv")