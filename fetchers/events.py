import os
import pathlib
import json
from fetchers.helpers import exists_in_db
import duckdb
import requests
import pandas as pd

class EventFetcher:
    def __init__(self, url: str, db: duckdb.DuckDBPyConnection) -> None:
        self.url = url
        self.db = db
        self.__init_events_db()

    def __init_events_db(self):
        self.db.sql(
            """CREATE TABLE events(
                id UUID,
                index INT,
                period INT,
                timestamp TIME,
                minute INT,
                second INT,
                type INT,
                possession INT,
                possession_team INT,
                play_pattern INT,
                team INT,
                player INT NULL,
                loc_x INT NULL,
                loc_y INT NULL,
                duration DECIMAL,
                under_pressure BOOL NULL,
                off_camera BOOL NULL,
                out BOOL NULL,
            )"""
        )

        self.db.sql(
            """CREATE TABLE event_type(
                id INT,
                name STRING
            )"""
        )

        self.db.sql(
            """CREATE TABLE play_pattern(
                id INT,
                name STRING
            )"""
        )

        self.db.sql(
            """CREATE TABLE players(
                id INT,
                name STRING
            )"""
        )

        self.db.sql(
            """CREATE TABLE related_events(
                id INT,
                event UUID
            )"""
        )

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



    def fetch(self, dir: str):
        rows = [x for x in pathlib.Path(dir).iterdir() if x.is_file()]

        for row in rows:
            fp = os.path.join(dir, row)
            print(fp)
            json_f = open(fp)
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

                self._check_for_event_type(event['type'])
                self._check_for_play_pattern(event['play_pattern'])
                if not event['player']['id'] == 'NULL':
                    self._check_for_player(event['player'])

    def _check_for_player(self, player: dict):
        id = player['id']
        name = player['name'].replace("'", "''")
        
        if exists_in_db('players', id, self.db) is False:
            self.db.sql(
                f"""
                INSERT INTO players VALUES(
                    {id},
                    '{name}',
                )
                """
            )

    def _check_for_play_pattern(self, play_pattern: dict):
        id = play_pattern['id']
        name = play_pattern['name']
        if exists_in_db('play_pattern', id, self.db) is False:
            self.db.sql(
                f"""
                INSERT INTO play_pattern VALUES(
                    {id},
                    '{name}',
                )
                """
            )

    def _check_for_event_type(self, event_type: dict):
        id = event_type['id']
        name = event_type['name']
        if exists_in_db('event_type', id, self.db) is False:
            self.db.sql(
                f"""
                INSERT INTO event_type VALUES(
                    {id},
                    '{name}',
                )
                """
            )
