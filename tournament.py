#tournament.py created November 19, 2016 by Christine Stoner

__copyright__ = """

    Copyright 2016 Christine Stoner

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.
       Returns a database connection.
    """
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect();
    cur = conn.cursor()
    #delete all matches
    cur.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect();
    cur = conn.cursor()
    # ensure no oustanding references from matches
    cur.execute("DELETE FROM matches")
    # delete all players
    cur.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect();
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM players")
    no_of_players = cur.fetchone()[0]
    conn.close()
    return no_of_players
    
def registerPlayer(name):
    """Adds a player to the tournament database.
      
    Args:
      name: the player's full name (need not be unique).
    """
    bleached_name = bleach.clean(name)
    conn = connect();
    cur = conn.cursor()
    query = "INSERT INTO players (name) VALUES(%s)"
    param = (bleached_name,)
    cur.execute(query, param)
    conn.commit()
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect();
    cur = conn.cursor()
    #ensure winner and loser are in database
    cur.execute("SELECT id FROM players")
    user_ids = cur.fetchall()
    print user_ids
    print winner
    print loser
    if (winner,) in user_ids and (loser,) in user_ids:
        #update matches table
        query = ("INSERT INTO matches (winning_player_id, losing_player_id)"
                 "VALUES (%s, %s)")
        param = (winner, loser)
        cur.execute(query, param)
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

    conn = connect();
    cur = conn.cursor()
    query = ("SELECT players.id, players.name, "
             "COALESCE(COUNT(matches.winning_player_id),0) AS wins "
             "FROM players LEFT OUTER JOIN matches ON "
             "players.id=matches.winning_player_id GROUP BY players.id"
             )
    cur.execute(query) 
    wins = cur.fetchall()
    second_query = ("SELECT players.id, "
             "COALESCE(COUNT(matches.losing_player_id),0) AS losses "
             "FROM players LEFT OUTER JOIN matches ON "
             "players.id=matches.losing_player_id GROUP BY players.id"
             )
    cur.execute(second_query)  
    losses = cur.fetchall()
    player_records = []
    

    for win in wins:
       for loss in losses:
            #when player_id matches
           if win [0]== loss[0]:
               player_record = win + (loss[1]+win[2],)
               player_records.append(player_record)
    sorted_player_records = sorted(player_records, 
                                   key = lambda x: x[2], reverse=True)
    print sorted_player_records
    return sorted_player_records

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

    currentStandings = playerStandings()
    list_size = len(currentStandings)
    new_list = []
    for i in range (0,list_size,2):
        a = (currentStandings[i][0],currentStandings[i][1])
        b = (currentStandings[i+1][0],currentStandings[i+1][1])
        c = a + b
        new_list.append(c)
    print new_list
    return new_list