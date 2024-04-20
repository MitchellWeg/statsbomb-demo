from io import StringIO
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
            """
            CREATE TABLE lineups(
                team_id INT,
                team_name STRING,
                lineup_players_id INT
            )
            """
        )

        self.db.sql(
            "CREATE SEQUENCE lineup_id_seq START 1"
        )
        self.db.sql(
            """
            CREATE TABLE lineup_player(
                id INT,
                player_id INT,
                jersey_number INT
            )
            """
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

                team_name = team_name.replace("'", "''")

                self.db.sql(
                    f"""
                    INSERT INTO lineups VALUES(
                        {team_id},
                        '{team_name}',
                        {next_id}
                    )
                    """
                )