import linear_weights_constants
import use_database
import sqlite3

def create_player_outcomes(player):
    return {"W": player.walks, "S": player.singles, "D": player.doubles, "T": player.triples, "H": player.home_runs, "O": player.at_bats - player.singles - player.doubles - player.triples - player.home_runs}

def update_player_raa(table_name):
    players = use_database.get_all_players(table_name)
    probabilities = use_database.get_league_stats(table_name)
    constants = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)

    # Making a connection between sqlite3 database and Python Program
    sqliteConnection = sqlite3.connect('baseball_data.db')
    # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
    # Otherwise it will show errors
    print("Connected to SQLite")

    cursor_obj = sqliteConnection.cursor()

    for player in players:
        outcomes = create_player_outcomes(player)
        player.RAA = linear_weights_constants.calculate_raa(constants, outcomes)
        insert_string = f"""
        UPDATE {table_name}
        SET RAA = {player.RAA}
        WHERE id = {player.id}
        """
        cursor_obj.execute(insert_string)

    sqliteConnection.commit()


    if sqliteConnection:
            # using close() method, we will close the connection
            sqliteConnection.close()
            # After closing connection object, we will print "the sqlite connection is closed"
            print("the sqlite connection is closed")

def get_woba_weights(linear_weights):
     o = -1 * linear_weights["O"]
     return {"W": linear_weights["W"] + o, "S": linear_weights["S"] + o, "D": linear_weights["D"] + o, "T": linear_weights["T"] + o, "H": linear_weights["H"] + o}

def get_league_woba(table_name):

    probabilities = use_database.get_league_stats(table_name)
    linear_weights = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)
    woba_weights = get_woba_weights(linear_weights)

    # Making a connection between sqlite3 database and Python Program
    sqliteConnection = sqlite3.connect('baseball_data.db')
    # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
    # Otherwise it will show errors
    print("Connected to SQLite")

    cursor_obj = sqliteConnection.cursor()

    select_string = f"""
        SELECT SUM(at_bats), SUM(singles), SUM(doubles), SUM(triples), SUM(hrs), SUM(walks) from {table_name}
        """
    
    cursor_obj.execute(select_string)

    output = cursor_obj.fetchall()
    
    if sqliteConnection:
        # using close() method, we will close the connection
        sqliteConnection.close()
        # After closing connection object, we will print "the sqlite connection is closed"
        print("the sqlite connection is closed")

    
    return (output[0][1] * woba_weights["S"] + output[0][2] * woba_weights["D"] + output[0][3] * woba_weights["T"] + output[0][4] * woba_weights["H"] + output[0][5] * woba_weights["W"]) / (output[0][0] + output[0][5])


def get_woba_scale(league_woba, desired_average = .300):
     return desired_average / league_woba

def calculate_player_woba(player_outcomes, woba_weights, woba_scale):
    total_pa = player_outcomes["W"] + player_outcomes["S"] + player_outcomes["D"] + player_outcomes["T"] + player_outcomes["H"] + player_outcomes["O"]
    unscaled_woba = (player_outcomes["W"] * woba_weights["W"] + player_outcomes["S"] * woba_weights["S"] + player_outcomes["D"] * woba_weights["D"] + player_outcomes["T"] * woba_weights["T"] + player_outcomes["H"] * woba_weights["H"]) / total_pa
    return unscaled_woba * woba_scale


def update_player_woba(table_name):
    players = use_database.get_all_players(table_name)
    probabilities = use_database.get_league_stats(table_name)
    constants = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)
    woba_weights = get_woba_weights(constants)
    league_woba = get_league_woba(table_name)
    woba_scale = get_woba_scale(league_woba)

    # Making a connection between sqlite3 database and Python Program
    sqliteConnection = sqlite3.connect('baseball_data.db')
    # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
    # Otherwise it will show errors
    print("Connected to SQLite")

    cursor_obj = sqliteConnection.cursor()

    for player in players:
        outcomes = create_player_outcomes(player)
        player.wOBA = calculate_player_woba(outcomes, woba_weights, woba_scale)
        insert_string = f"""
        UPDATE {table_name}
        SET woba = {player.wOBA}
        WHERE id = {player.id}
        """
        cursor_obj.execute(insert_string)

    sqliteConnection.commit()


    if sqliteConnection:
            # using close() method, we will close the connection
            sqliteConnection.close()
            # After closing connection object, we will print "the sqlite connection is closed"
            print("the sqlite connection is closed")

if __name__ == "__main__":
     update_player_raa("rock_2022")
     league_woba = get_league_woba("rock_2022")
     print(league_woba)
     update_player_woba("rock_2022")