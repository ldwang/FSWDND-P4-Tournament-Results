#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from matches;"
    db_cursor.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from players;"
    db_cursor.execute(query)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "select count(id) as num from players"
    db_cursor.execute(query)
    results = db_cursor.fetchone()
    conn.close()
    if results:
        return results[0]
    else:
        return '0'

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    db_cursor.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    db_cursor = conn.cursor()
    # A query using subquery with left join to show the standings on the descend order.
    query = "select t1.id, t1.name, t2.wins, t1.matches from total_matches t1 left join \
  (select players.id, players.name, count(matches.winner) as wins from players LEFT JOIN matches \
  ON players.id=matches.winner group by players.id ) t2 on t1.id=t2.id order by wins DESC;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    conn.close()
    if results:
        return results
    else:
        return []


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    db_cursor.execute(query, (winner, loser))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    results = []
    if standings:
        num_players = len(standings)
        for i in xrange(0, num_players/2):
            (id1, name1, id2, name2) = (standings[2*i][0], standings[2*i][1], standings[2*i+1][0], standings[2*i+1][1])
            results.append((id1,name1,id2,name2))

    return results



