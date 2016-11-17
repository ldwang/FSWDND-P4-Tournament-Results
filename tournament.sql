-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;

create DATABASE tournament;

\c tournament;

create table players (id SERIAL PRIMARY KEY,
                      name TEXT);

create table matches (id SERIAL PRIMARY KEY,
                      winner INTEGER REFERENCES players (id),
                      loser INTEGER REFERENCES players(id));

-- create a view for showing each players id, name and total matches
create view total_matches as select players.id, players.name, count(matches.id) as matches
                             from players left join matches
                             ON players.id=matches.winner or players.id=matches.loser
                             GROUP BY players.id;