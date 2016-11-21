## Tournament Application

This psql database setup sets up a database and then provides the following functions to perform a swiss pairing tournament:

* deleteMatches() - deletes all matches
* deletePlayers() - deletes all players
* countPlayers() - returns players currently registered
* registerPlayer(name) - registers a player (parameter name)
* reportMatch(winner, loser) - records the result of a match when given winning and losing player id
*  playerStandings() - returns a list of the players and their win records, sorted by wins.
* swissPairings() - Returns a list of pairs of players for the next round of a match.

### Installation, or How To Run

1.  Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/).
2.  Ensure vagrant/python has [psycopg](http://initd.org/psycopg/) and [bleach](https://pypi.python.org/pypi/bleach)
3.  Download the git repository [here](https://github.com/acct252000/udacity_relational_database) by clicking on the green button.  Download to a file accessible by your vagrant virtual machine.
4.  Launch the vagrant machine by typing `vagrant up.` in the command line from the vagrant directory.
5.  Type `vagrant ssh.`
6.  Type `psql`.
7.  Create a database by typing `create database tournament;`.
8.  Connect to the tournament database by typing `\connect tournament`.
9.  Copy and paste the first create table statement from the tournament.sql file into the command line and hit enter.
10. Copy and paste the second create table statement from the tournament.sql file into the command line and hit enter.
11.  Type `\q` to exit psql.
12.  Type `python tournament_test.py` to run test file.

### Attributions

* Sorting a python list in descending order from [stackoverflow](http://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value)
