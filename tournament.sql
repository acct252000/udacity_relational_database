-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
-- table to hold player information, including name, timestamp, id, score, matches_played, and win_percentage
CREATE TABLE players ( name TEXT,
                       time_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       id SERIAL primary key
                       );

-- table to hold match information, including match id, round, first and second player id, and winning player id
CREATE TABLE matches ( match_id SERIAL primary key,
			                 winning_player_id INTEGER references players (id),
                       losing_player_id INTEGER references players (id)
                     );