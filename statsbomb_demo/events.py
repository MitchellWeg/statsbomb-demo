import os
import pathlib
import json
from helpers import exists_in_db, clean_str, read_sql_file
import duckdb
import requests
from threading import Thread

class EventFetcher:
    def __init__(self, url: str, db: duckdb.DuckDBPyConnection) -> None:
        self.url = url
        self.db = db


    def download(self, out_dir: str):
        q = "SELECT id FROM matches"

        rows = self.db.sql(q).fetchall()

        for row in rows:
            match_id = str(row[0])
            q = self.url.replace('{match_id}', match_id)
            all_events = requests.get(q).json()

            with open(os.path.join(out_dir, match_id), 'w') as f:
                events = [json.dumps(x, indent=4) for x in all_events]
                s = ",".join(events)
                s = f'[{s}]'
                f.write(s)


    def fetch(self, dir: str, thread_count: int):
        rows = [x for x in pathlib.Path(dir).iterdir() if x.is_file()]
        if thread_count > 1:
            chunk_size = len(rows) // thread_count
            out = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)] 
            threads = []

            for o in out:
                conn = duckdb.connect('statsbomb.db')
                threads.append(
                    Thread(target=self._fetch,
                        args=(dir,o, conn))
                )

            print("thread amount: " + str(len(threads)))
            print("work amount: " + str(len(out)))

            for t in threads:
                t.start()

            for t in threads:
                t.join()
        else:
            self._fetch(dir, rows, self.db)


    def _fetch(self, dir: str, rows: list, conn: duckdb.DuckDBPyConnection):
        for row in rows:
            fp = os.path.join(dir, row)
            print(fp)
            with open(fp) as json_f:
                all_events = json.load(json_f)

                for event in all_events:
                    event_name = event['type']['name']
                    if event_name in [
                        "Starting XI", "Half Start", "Half End", "Tactical Shift",
                        "Own Goal For"
                    ]:
                        continue

                    if 'location' not in event.keys():
                        event['location'] = []
                        event['location'].append("NULL")
                        event['location'].append("NULL")

                    if 'duration' not in event.keys():
                        event['duration'] = 0

                    if 'under_pressure' not in event.keys():
                        event['under_pressure'] = 'NULL'

                    if 'off_camera' not in event.keys():
                        event['off_camera'] = 'NULL'

                    if 'out' not in event.keys():
                        event['out'] = 'NULL'

                    if 'player' not in event.keys():
                        event['player'] = {'id': 'NULL'}

                    self.db.sql(
                        f"""
                        INSERT INTO events VALUES(
                            '{event['id']}',
                            {event['index']},
                            {event['period']},
                            '{event['timestamp']}',
                            {event['minute']},
                            {event['second']},
                            {event['type']['id']},
                            {event['possession']},
                            {event['possession_team']['id']},
                            {event['play_pattern']['id']},
                            {event['team']['id']},
                            {event['player']['id']},
                            {event['location'][0]},
                            {event['location'][1]},
                            {event['duration']},
                            {event['under_pressure']},
                            {event['off_camera']},
                            {event['out']},
                        )
                        """
                    )

                    self._check_for_event_type(event['type'], conn)
                    self._check_for_play_pattern(event['play_pattern'], conn)
                    if not event['player']['id'] == 'NULL':
                        self._check_for_player(event['player'], conn)

    def _check_for_player(self, player: dict, conn: duckdb.DuckDBPyConnection):
        id = player['id']
        name = clean_str(player['name'])
        
        if exists_in_db('players', id, conn) is False:
            self.db.sql(
                f"""
                INSERT INTO players VALUES(
                    {id},
                    '{name}',
                )
                """
            )

    def _check_for_play_pattern(self, play_pattern: dict, conn: duckdb.DuckDBPyConnection):
        id = play_pattern['id']
        name = play_pattern['name']
        if exists_in_db('play_pattern', id, conn) is False:
            self.db.sql(
                f"""
                INSERT INTO play_pattern VALUES(
                    {id},
                    '{name}',
                )
                """
            )

    def _check_for_event_type(self, event_type: dict, conn: duckdb.DuckDBPyConnection ):
        id = event_type['id']
        name = event_type['name']
        if exists_in_db('event_type', id, conn) is False:
            self.db.sql(
                f"""
                INSERT INTO event_type VALUES(
                    {id},
                    '{name}',
                )
                """
            )
