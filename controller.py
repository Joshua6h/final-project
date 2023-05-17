import parsestats
import alchemy
import calculateleaguewidestats
import linear_weights_constants

def create_league(league_name):
    players = parsestats.parse_data(league_name + '.csv')
    if players == False:
        return False

    p = alchemy.Players()
    for player in players:
        p.writeData(player, league_name)

    return True


def update_player_raa(players, constants):
    for player in players:
        outcomes = calculateleaguewidestats.create_player_outcomes(player)
        player.RAA = linear_weights_constants.calculate_raa(constants, outcomes)
        alchemy.update_player_RAA(player)

def get_woba_weights(linear_weights):
     """Function to convert basic linear weights to linear weights for calculating wOBA"""
     o = -1 * linear_weights["O"]
     return {"W": linear_weights["W"] + o, "S": linear_weights["S"] + o, "D": linear_weights["D"] + o, "T": linear_weights["T"] + o, "H": linear_weights["H"] + o}

def get_league_woba(woba_weights, league_name):
    """Gets the league wide wOBA without weighting it in order to normalize it"""
    # probabilities = use_database.get_league_stats(table_name)
    # linear_weights = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)
    # woba_weights = get_woba_weights(linear_weights)

    players = alchemy.Players()

    output = players.readLeagueWideStats(league_name)
    

    
    return (output[1] * woba_weights["S"] + output[2] * woba_weights["D"] + output[3] * woba_weights["T"] + output[4] * woba_weights["H"] + output[5] * woba_weights["W"]) / (output[0] + output[5])


def get_woba_scale(league_woba, desired_average = .300):
     """Returns the wOBA scale to multiply unweighted player wOBAs by"""
     return desired_average / league_woba

def calculate_player_woba(player_outcomes, woba_weights, woba_scale):
    """Calculates the weighted on base average for a player"""
    total_pa = player_outcomes["W"] + player_outcomes["S"] + player_outcomes["D"] + player_outcomes["T"] + player_outcomes["H"] + player_outcomes["O"]
    # players with no plate appearances will be listed to have a 0 woba
    if total_pa == 0:
        return 0
    unscaled_woba = (player_outcomes["W"] * woba_weights["W"] + player_outcomes["S"] * woba_weights["S"] + player_outcomes["D"] * woba_weights["D"] + player_outcomes["T"] * woba_weights["T"] + player_outcomes["H"] * woba_weights["H"]) / total_pa
    return unscaled_woba * woba_scale

def update_player_woba(players, constants, table_name):
    """Updates wOBA for all players in a table"""
    # players = use_database.get_all_players(table_name)
    # probabilities = use_database.get_league_stats(table_name)
    # constants = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)
    woba_weights = get_woba_weights(constants)
    league_woba = get_league_woba(woba_weights, table_name)
    woba_scale = get_woba_scale(league_woba)

    for player in players:
        outcomes = calculateleaguewidestats.create_player_outcomes(player)
        player.wOBA = calculate_player_woba(outcomes, woba_weights, woba_scale)
        alchemy.update_player_wOBA(player)

def overwrite_league(league_name):
    alchemy.delete_league(league_name)
    league_success = create_league(league_name)
    if not league_success:
        return False

    update_all_stats(league_name)
    return True

def update_all_stats(table_name):
    players = alchemy.get_filtered_sorted_players(table_name)
    probabilities = alchemy.get_league_stats(table_name)
    constants = linear_weights_constants.get_linear_weights_constants(10e-8, probabilities)

    update_player_raa(players, constants)
    update_player_woba(players, constants, table_name)
    
    
if __name__ == "__main__":
    overwrite_league("rock_2022")