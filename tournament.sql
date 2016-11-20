-- Table definitions for the tournament project.


-- table to hold player information, including name, timestamp, id, score, matches_played, and win_percentage
CREATE TABLE players ( name TEXT,
                       time_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       id SERIAL primary key,
                       score NUMERIC,
                       matches_played NUMERIC,
                       win_percentage NUMERIC);

-- table to hold match information, including match id, round, first and second player id, and winning player id
CREATE TABLE matches ( name TEXT,
			  match_id SERIAL primary key,
			  round INTEGER NOT NULL,
			  first_player_id INTEGER references players (id),
                       second_player_id INTEGER references players (id),
                       winning_player_id INTEGER references players (id)
                     );



