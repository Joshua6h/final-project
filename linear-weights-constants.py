import re24
import constants

def get_linear_weights_constants(min_prob, probabilities):
    run_scoring_environment = re24.get_run_scoring_environment(min_prob, probabilities)
    re24matrix = run_scoring_environment[0]
    probs_matrix = run_scoring_environment[1]

    linear_weights = {"W": 0, "S": 0, "D": 0, "T": 0, "H": 0, "O": 0}

    for outcome in linear_weights:
        re = 0
        for situation in probs_matrix:
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
    raa = 0
    for outcome in outcomes:
        raa += linear_weights_constants[outcome] * outcomes[outcome]

    return raa

if __name__ == '__main__':
    # 2010-2015 MLB environment
    probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
    # run_scoring_environment = re24.get_run_scoring_environment(10e-8, probabilities)
    # print(run_scoring_environment)
    linear_weights_constants = get_linear_weights_constants(10e-8, probabilities)
    # print(linear_weights_constants)

    # Ryan Braun 2011 stats
    ryan_braun_2011 = {"W": 63, "S": 110, "D": 38, "T": 6, "H": 33, "O": 376}
    ryan_braun_raa_2011 = calculate_raa(linear_weights_constants, ryan_braun_2011)
    print("Ryan Braun 2011: " + str(ryan_braun_raa_2011))


    # Ryan Braun 2012 stats
    ryan_braun_2012 = {"W": 74, "S": 111, "D": 36, "T": 3, "H": 41, "O": 486}
    ryan_braun_raa_2012 = calculate_raa(linear_weights_constants, ryan_braun_2012)
    print("Ryan Braun 2012: " + str(ryan_braun_raa_2012))