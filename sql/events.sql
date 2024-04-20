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
    out BOOL NULL,
);


CREATE TABLE event_type(
    id INT,
    name STRING
);


CREATE TABLE play_pattern(
    id INT,
    name STRING
);


CREATE TABLE players(
    id INT,
    name STRING
);


CREATE TABLE related_events(
    id INT,
    event UUID
);