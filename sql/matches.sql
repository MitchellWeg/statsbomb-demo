CREATE TABLE stadiums(id INT, name STRING, country_id INT);
CREATE TABLE countries(id INT, name STRING);
CREATE TABLE referees(id INT, name STRING, country_id INT);
CREATE TABLE teams(id INT, name STRING, gender STRING, country_id INT, managers_id INT);
CREATE TABLE manager(id INT, name STRING, nickname STRING, dob STRING, country_id INT);

CREATE TABLE managers(id INT, team_id INT, manager_id INT);
CREATE TABLE matches(
            id INT,
            match_date DATE,
            kick_off TIME NULL,
            season_id INT,
            season_name STRING,
            home_team_id INT,
            away_team_id INT,
            home_team_score INT,
            away_team_score INT,
            match_status STRING,
            match_status_360 STRING,
            last_updated DATE,
            last_updated_360 STRING,
            data_version STRING,
            shot_fidelity_version INT,
            xy_fidelity_version INT,
            match_week INT,
            competition_stage STRING,
);