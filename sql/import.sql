COPY countries
FROM '/home/data/countries.csv'
DELIMITER ','
CSV HEADER;

COPY event_type
FROM '/home/data/event_type.csv'
DELIMITER ','
CSV HEADER;

COPY events
FROM '/home/data/events.csv'
DELIMITER ','
CSV HEADER;

COPY lineup_player
FROM '/home/data/lineup_player.csv'
DELIMITER ','
CSV HEADER;

COPY lineups
FROM '/home/data/lineups.csv'
DELIMITER ','
CSV HEADER;

COPY manager
FROM '/home/data/manager.csv'
DELIMITER ','
CSV HEADER;

COPY managers
FROM '/home/data/managers.csv'
DELIMITER ','
CSV HEADER;

COPY matches
FROM '/home/data/matches.csv'
DELIMITER ','
CSV HEADER;

COPY play_pattern
FROM '/home/data/play_pattern.csv'
DELIMITER ','
CSV HEADER;

COPY players
FROM '/home/data/players.csv'
DELIMITER ','
CSV HEADER;

COPY referees
FROM '/home/data/referees.csv'
DELIMITER ','
CSV HEADER;

COPY related_events
FROM '/home/data/related_events.csv'
DELIMITER ','
CSV HEADER;

COPY stadiums
FROM '/home/data/stadiums.csv'
DELIMITER ','
CSV HEADER;

COPY teams
FROM '/home/data/teams.csv'
DELIMITER ','
CSV HEADER;