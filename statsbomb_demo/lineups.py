from helpers import clean_str, read_sql_file
import requests
import os
import pathlib
import duckdb

class LineupFetcher:
    def __init__(self, url: str, db: duckdb.DuckDBPyConnection) -> None:
        self.db = db
        self.url = url
        self.__init_db()

    def __init_db(self):
        self.db.sql(
            "CREATE SEQUENCE lineup_id_seq START 1"
        )


    def fetch(self, dir: str):
        rows = [x for x in pathlib.Path(dir).iterdir() if x.is_file()]

        for row in rows:
            name = os.path.basename(row)
            url = self.url.replace('{match_id}', name)
            r = requests.get(url).json()

            for lineup in r:
                team_id = lineup['team_id']
                team_name = lineup['team_name']
                lu = lineup['lineup']

                for player in lu:
                    player_id = player['player_id']
                    jersey_number = player['jersey_number']

                    next_id = self.db.sql(
                        "SELECT nextval('lineup_id_seq')"
                    ).fetchone()[0]

                    self.db.sql(
                        f"""
                        INSERT INTO lineup_player VALUES(
                            {next_id},
                            {player_id},
                            {jersey_number},
                        )
                        """
                    )

                team_name = clean_str(team_name)

                self.db.sql(
                    f"""
                    INSERT INTO lineups VALUES(
                        {team_id},
                        '{team_name}',
                        {next_id}
                    )
                    """
                )
