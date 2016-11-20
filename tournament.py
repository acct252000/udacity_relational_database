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
    cur.execute("delete from matches")
    #remove match history from player file
    cur.execute("update players set matches_played = 0, score=0, "
                "win_percentage=0")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect();
    cur = conn.cursor()
    # ensure no oustanding references from matches
    cur.execute("delete from matches")
    # delete all players
    cur.execute("Delete from players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect();
    cur = conn.cursor()
    cur.execute("select count(id) from players")
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
    cur.execute("insert into players (name, score, matches_played, "
                "win_percentage) values(%s,0,0,0)",(bleached_name,))
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
    #update winner
    cur.execute("update players set score = score +1, "
                "matches_played = matches_played+1 "
                "where id = %s",(winner,))
    #update loser
    cur.execute("update players set matches_played = matches_played+1 "
                "where id = %s",(loser,))
    #update match table
    cur.execute("update matches set winning_player_id = %s where "
                "(first_player_id = %s AND second_player_id = %s) "
                "OR (first_player_id = %s AND second_player_id = %s)",
                (winner, winner,loser,loser,winner))
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
    cur.execute("select players.id, players.name, players.score, "
                "players.matches_played from players order by players.score "
                "DESC") 
    rows= cur.fetchall()
    
    return rows

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
    conn = connect();
    cur = conn.cursor()
    #determine round by selecting max round from matches table
    cur.execute("select coalesce(max(round),0) from matches")
    max_round = cur.fetchone()[0]
    # if nothing in table generate first round matches
    if max_round == 0:
        cur.execute("select players.id, players.name from players")
        rows = cur.fetchall()
        list_size = len(rows)
        new_list = []
        for i in range (0,list_size,2):
            a = rows[i]
            b = rows[i+1]
            #add match to matches table
            cur.execute("insert into matches (first_player_id, "
                        "second_player_id, round) values(%s,%s,1)",
                         (a[0],b[0]))
            c = a + b
            new_list.append(c)
        conn.commit()
        conn.close()
    #if one round played generate matches for next round
    else:
        round = max_round +1
        # update win percentages all players
        cur.execute("update players set win_percentage = score/matches_played"
                    " where matches_played > 0")
        conn.commit()
        # order by win percentages
        cur.execute("select players.id, players.name from players order by "
                    "players.win_percentage DESC")
        rows = cur.fetchall()
        list_size = len(rows)
        new_list = []
        for i in range (0,list_size,2):
            a = rows[i]
            b = rows[i+1]
            cur.execute("insert into matches (first_player_id, "
                        "second_player_id, round) values(%s,%s,%s)",
                        (a[0],b[0],round))
            c = a + b
            new_list.append(c)
        conn.commit()
        conn.close()
    print new_list
    return new_list
    
   
