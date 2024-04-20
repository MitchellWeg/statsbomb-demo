import requests
import duckdb
from helpers import exists_in_db, clean_str, read_sql_file

class MatchesFetcher():
    def __init__(self, url: str, db: duckdb.DuckDBPyConnection) -> None:
        self.url = url
        self.db = db
        self.__init_matches_db()

    def __init_matches_db(self):
        self.db.sql("CREATE SEQUENCE seq_managers_id START 1")

    
    def fetch(self, competition_id: int, season_id: int):
        url = self.url.replace('{competition_id}', str(competition_id)).replace('{season_id}', str(season_id))
        match_json = requests.get(url).json()

        for match in match_json:
            new_data = {}

            for key in match.keys():
                if type(match[key]) is not dict and type(match[key]) is not list:
                    new_data[key] = match[key]
                else:
                    if key == 'competition_stage':
                        new_data['competition_stage'] = match['competition_stage']['name']
                    if key == 'metadata':
                        new_data = new_data | match['metadata']
                    if key == 'season':
                        new_data = new_data | match['season']
                    if key == 'stadium':
                        self.handle_stadium(match[key])
                    if key == 'referee':
                        self.handle_referee(match[key])
                    if key == 'home_team':
                        new_data['home_team_id'] = match[key]['home_team_id']
                        self.handle_team(match[key], 'home')
                    if key == 'away_team':
                        new_data['away_team_id'] = match[key]['away_team_id']
                        self.handle_team(match[key], 'away')

            if not 'shot_fidelity_version' in match.keys():
                new_data['shot_fidelity_version'] = "NULL"

            if not 'xy_fidelity_version' in match.keys():
                new_data['xy_fidelity_version'] = "NULL"

            if not 'data_version' in match.keys():
                new_data['data_version'] = "NULL"

            if not 'match_status_360' in match.keys():
                new_data['match_status_360'] = "NULL"

            kick_off_time = new_data['kick_off']
            kick_off_time = f"'{kick_off_time}'" if kick_off_time else 'NULL'

            q = f"""INSERT INTO matches VALUES(
                    {new_data['match_id']},
                    '{new_data['match_date']}',
                    {kick_off_time},
                    {new_data['season_id']},
                    '{new_data['season_name']}',
                    {new_data['home_team_id']},
                    {new_data['away_team_id']},
                    {new_data['home_score']},
                    {new_data['away_score']},
                    '{new_data['match_status']}',
                    '{new_data['match_status_360']}',
                    '{new_data['last_updated']}',
                    NULL,
                    '{new_data['data_version']}',
                    {new_data['shot_fidelity_version']},
                    {new_data['xy_fidelity_version']},
                    {new_data['match_week']},
                    '{new_data['competition_stage']}',
                )"""

            self.db.sql(q)

    def handle_team(self, team: dict, side: str):
        prefix = f'{side}_team'
        team_id = team[f'{prefix}_id']
        team_name = team[f'{prefix}_name']
        team_gender = team[f'{prefix}_gender']
        team_country_id = team['country']['id']
        team_managers = []
        if 'managers' in team.keys():
            team_managers = team['managers']
        r = self.db.sql(f"select * from teams where id = {team_id}")

        for manager in team_managers:
            manager_id = manager['id']

            if not exists_in_db('manager', manager_id, self.db):
                nickname = manager['nickname']
                dob = manager['dob']
                q = f"""insert into manager values(
                        {manager_id},
                        '{manager['name']}',
                        '{nickname if nickname is not None else "NULL"}',
                        {dob if dob else "NULL"},
                        {manager['country']['id']},
                    )"""


                self.db.sql(
                    q
                )

            man_teams_id = self.db.sql("select nextval('seq_managers_id')").fetchone()[0]

            self.db.sql(
                f"""insert into managers values(
                    {man_teams_id},
                    {team_id},
                    {manager_id}
                )"""
            )

        if not r.fetchone():
            managers_id_teams = None
            if len(team_managers) > 0:
                q = f'SELECT id FROM managers WHERE team_id = {team_id} AND manager_id = {team_managers[0]["id"]}'
                managers_id_teams = self.db.sql(q).fetchone()
            team_name = clean_str(team_name)
            insert = "insert into teams values(?, ?, ?, ?, ?)"

            self.db.execute(insert, (
                        team_id, 
                        team_name, 
                        team_gender, 
                        team_country_id,
                        managers_id_teams[0] if managers_id_teams is not None else "-1"
                )
            )

        self.handle_countries(team['country'])

    def handle_referee(self, referee: dict):
        r = self.db.sql(f"select * from referees where id = {referee['id']}")

        if not r.fetchone():
            self.db.sql(f"insert into referees values({referee['id']}, '{referee['name']}', {referee['country']['id']})")

        self.handle_countries(referee['country'])

    def handle_stadium(self, stadium: dict):
        r = self.db.sql(f"select * from stadiums where id = {stadium['id']}")

        if not r.fetchone():
            name = clean_str(stadium['name'])
            q = f"insert into stadiums values({stadium['id']}, '{name}', {stadium['country']['id']})"
            self.db.sql(q)

        self.handle_countries(stadium['country'])

    def handle_countries(self, country: dict):
        r = self.db.sql(f"select * from countries where id = {country['id']}")
        name = clean_str(country['name'])

        if not r.fetchone():
            self.db.sql(f"insert into countries values({country['id']}, '{name}')")



