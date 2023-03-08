import search
import constants

def actions(state):
    return ["O", "W", "S", "D", "T", "H", "P"]

def result(state, action):
    return constants.result_dictionary[state][action]

def action_cost(state, action, new_state):
    return 0

# Helper function to create a dictionary of all 24 possible states and the run expectancy for each state
def get_re24_matrix(problem):
    re_matrix = {
        ("a", 0): 0,
        ("a", 1): 0,
        ("a", 2): 0,
        ("b", 0): 0,
        ("b", 1): 0,
        ("b", 2): 0,
        ("c", 0): 0,
        ("c", 1): 0,
        ("c", 2): 0,
        ("d", 0): 0,
        ("d", 1): 0,
        ("d", 2): 0,
        ("e", 0): 0,
        ("e", 1): 0,
        ("e", 2): 0,
        ("f", 0): 0,
        ("f", 1): 0,
        ("f", 2): 0,
        ("g", 0): 0,
        ("g", 1): 0,
        ("g", 2): 0,
        ("h", 0): 0,
        ("h", 1): 0,
        ("h", 2): 0,
    }

    for item in re_matrix.items():
        problem.initial = item[0]
        re_matrix[item[0]] = search.get_run_expectancy(problem)

    return re_matrix

# function to return ordered pair of run expectancy matrix dictionary and state probability dictionary
def get_run_scoring_environment(min_prob, probabilities):
    problem = search.Problem(("a", 0), min_prob, result, actions, action_cost, probabilities)
    re24_matrix = get_re24_matrix(problem)
    problem.initial = ("a", 0)
    probability_matrix = search.get_probabilities(problem)
    return (re24_matrix, probability_matrix)

if __name__ == '__main__':
    # test code will take stats from MLB 2010-2015
    # compare the RE24 matrix to the one shown in this article:
    # https://library.fangraphs.com/principles/linear-weights/
    probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
    initial = ("a", 0)
    problem = search.Problem(initial, 10e-8, result, actions, action_cost, probabilities)

    re24_matrix = get_re24_matrix(problem)
    print(re24_matrix)