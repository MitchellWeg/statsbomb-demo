CREATE TABLE events(
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
    out BOOL NULL
);


CREATE TABLE event_type(
    id INT,
    name VARCHAR(255)
);


CREATE TABLE play_pattern(
    id INT,
    name VARCHAR(255)
);


CREATE TABLE players(
    id INT,
    name VARCHAR(255)
);


CREATE TABLE related_events(
    id INT,
    event UUID
);


CREATE TABLE lineups(
    team_id INT,
    team_name VARCHAR(255),
    lineup_players_id INT
);


CREATE TABLE lineup_player(
    id INT,
    player_id INT,
    jersey_number INT
);


CREATE TABLE stadiums(id INT, name VARCHAR(255), country_id INT);
CREATE TABLE countries(id INT, name VARCHAR(255));
CREATE TABLE referees(id INT, name VARCHAR(255), country_id INT);
CREATE TABLE teams(id INT, name VARCHAR(255), gender VARCHAR(255), country_id INT, managers_id INT);
CREATE TABLE manager(id INT, name VARCHAR(255), nickname VARCHAR(255), dob VARCHAR(255), country_id INT);

CREATE TABLE managers(id INT, team_id INT, manager_id INT);
CREATE TABLE matches(
            id INT,
            match_date DATE,
            kick_off TIME NULL,
            season_id INT,
            season_name VARCHAR(255),
            home_team_id INT,
            away_team_id INT,
            home_team_score INT,
            away_team_score INT,
            match_status VARCHAR(255),
            match_status_360 VARCHAR(255),
            last_updated DATE,
            last_updated_360 VARCHAR(255),
            data_version VARCHAR(255),
            shot_fidelity_version INT,
            xy_fidelity_version INT,
            match_week INT,
            competition_stage VARCHAR(255)
);