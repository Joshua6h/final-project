import re24
import constants

def get_linear_weights_constants(min_prob, probabilities):
    """function to calculate linear weights constants"""
    run_scoring_environment = re24.get_run_scoring_environment(min_prob, probabilities)
    re24matrix = run_scoring_environment[0]
    probs_matrix = run_scoring_environment[1]

    linear_weights = {"W": 0, "S": 0, "D": 0, "T": 0, "H": 0, "O": 0}

    for outcome in linear_weights:
        # for each possible outcome, calculate average change in run expectancy
        re = 0
        for situation in probs_matrix:
            # for each game state, multiply relative probability of being in that game state by
            # the change in run expectancy caused by the event
            old_re = re24matrix[situation]
            result = constants.result_dictionary[situation][outcome]
            if result[0][1] < 3:
                new_re = re24matrix[result[0]] + result[1]
            else:
                new_re = 0
            re += (new_re - old_re) * probs_matrix[situation]
        
        linear_weights[outcome[0]] = re

    return linear_weights


def calculate_raa(linear_weights_constants, outcomes):
    """helper function to calculate runs above average using the linear weights constants"""
    raa = 0
    for outcome in outcomes:
        raa += linear_weights_constants[outcome] * outcomes[outcome]

    return raa


def create_test_case(walks, hits, doubles, triples, hr, ab):
    """helper function to create a test case for a player"""
    return {"W": walks, "S": hits - doubles - triples - hr, "D": doubles, "T": triples, "H": hr, "O": ab - hits}


def create_test_season(w, hbp, hits, doubles, triples, hr, pa):
    """helper function to create the run scoring environment for a season"""
    probabilities = {"W": 0, "S": 0, "D": 0, "T": 0, "H": 0, "O": 0, "P": 0}
    probabilities["W"] = (w + hbp) / pa
    probabilities["S"] = (hits - doubles - triples - hr) / pa
    probabilities["D"] = doubles / pa
    probabilities["T"] = triples / pa
    probabilities["H"] = hr / pa
    total_outs = pa - hits - w -hbp
    # assume 2% of outs score runner from third
    probabilities["P"] = .02 * (total_outs) / pa
    probabilities["O"] = .98 * (total_outs) / pa
    return probabilities

def create_season(ab, singles, doubles, triples, hrs, walks):
    """helper function to create the run scoring environment for a season"""
    pa = ab + walks
    probabilities = {"W": 0, "S": 0, "D": 0, "T": 0, "H": 0, "O": 0, "P": 0}
    probabilities["W"] = (walks) / pa
    probabilities["S"] = singles / pa
    probabilities["D"] = doubles / pa
    probabilities["T"] = triples / pa
    probabilities["H"] = hrs / pa
    total_outs = pa - singles - doubles - triples - hrs - walks
    # assume 2% of outs score runner from third
    probabilities["P"] = .02 * (total_outs) / pa
    probabilities["O"] = .98 * (total_outs) / pa
    return probabilities

if __name__ == '__main__':
    # 2010-2015 MLB environment
    probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
    # run_scoring_environment = re24.get_run_scoring_environment(10e-8, probabilities)
    # print(run_scoring_environment)
    # linear_weights_constants = get_linear_weights_constants(10e-8, probabilities)
    # print(linear_weights_constants)

    # Mike Trout 2015 - actual RAA = 68
    mike_trout = create_test_case(102, 172, 32, 6, 41, 575)

    # Actual linear weights - 2015
    linear_weights_constants = {"W": .3, "S": .44, "D": .74, "T": 1.01, "H": 1.39, "O": -.26}
    print("Actual linear weights constants from 2015:")
    print(linear_weights_constants)


    # My 2015 linear weights constants
    probabilities = create_test_season(14073, 1602, 42106, 8242, 939, 4909, 183628)
    linear_weights_constants = get_linear_weights_constants(10e-8, probabilities)
    print("My linear weights:")
    print(linear_weights_constants)
    mike_trout_raa = calculate_raa(linear_weights_constants, mike_trout)
    print("Mike Trout: " + str(mike_trout_raa))

    # Martin Maldonado 2015 - actual RAA = -4
    martin_maldonado = create_test_case(24, 48, 7, 0, 4, 229)
    martin_maldonado_raa = calculate_raa(linear_weights_constants, martin_maldonado)
    print("Martin Maldonado: " + str(martin_maldonado_raa))


    # Ryan Braun 2011 stats
    # ryan_braun_2011 = create_test_case(63, 187, 38, 6, 33, 563)
    # ryan_braun_2011 = create_test_case(63, 187, 38, 6, 33, 563)
    # ryan_braun_raa_2011 = calculate_raa(linear_weights_constants, ryan_braun_2011)
    # print("Ryan Braun 2011: " + str(ryan_braun_raa_2011))


    # Ryan Braun 2012 stats
    # ryan_braun_2012 = create_test_case(74, 191, 36, 3, 41, 598)
    # ryan_braun_2012 = {"W": 74, "S": 111, "D": 36, "T": 3, "H": 41, "O": 407}
    # ryan_braun_raa_2012 = calculate_raa(linear_weights_constants, ryan_braun_2012)
    # print("Ryan Braun 2012: " + str(ryan_braun_raa_2012))

    # 2022 Rock River League Stats
    print("2022 Rock River League Stats")
    probabilities = create_test_season(1146, 278, 2391, 357, 30, 113, 9833)
    linear_weights_constants = get_linear_weights_constants(10e-8, probabilities)
    print(linear_weights_constants)

    # Josh Hennen
    josh_hennen = create_test_case(6, 9, 1, 0, 0, 40)
    josh_hennen_raa = calculate_raa(linear_weights_constants, josh_hennen)
    print("Josh Hennen: " + str(josh_hennen_raa))

    # Aaron Roeseler
    aaron_roeseler = create_test_case(6, 40, 3, 0, 1, 78)
    aaron_roeseler_raa = calculate_raa(linear_weights_constants, aaron_roeseler)
    print("Aaron Roeseler: " + str(aaron_roeseler_raa))