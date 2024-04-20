import duckdb

class Dumper:
    def __init__(self, out: str, conn: duckdb.DuckDBPyConnection):
        self.out = out
        self.conn = conn

    def dump(self):
        tables = ["countries", "events", "event_type", "lineup_player", "lineups", "manager", "managers", "matches", "play_pattern", "players", "referees", "related_events", "stadiums", "teams"]

        for table in tables:
            self.conn.sql(
                f"""
                COPY {table} TO '{self.out}/{table}.csv' (HEADER, DELIMITER ',');
                """
            )
