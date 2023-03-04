import search

def actions(state):
    return ["O", "W", "S", "D", "T", "H", "P"]
    # return ["O", "W", "S", "D", "T", "H"]


def result(state, action):
    result_dictionary = {
        # nobody on, 0 outs
        ("a", 0): {
            "O": (("a", 1), 0),
            "P": (("a", 1), 0),
            "K": (("a", 1), 0),
            "W": (("b", 0), 0),
            "S": (("b", 0), 0),
            "D": (("c", 0), 0),
            "T": (("d", 0), 0),
            "H": (("a", 0), 1),
        },

        # nobody on, 1 out
        ("a", 1): {
            "O": (("a", 2), 0),
            "P": (("a", 2), 0),
            "K": (("a", 2), 0),
            "W": (("b", 1), 0),
            "S": (("b", 1), 0),
            "D": (("c", 1), 0),
            "T": (("d", 1), 0),
            "H": (("a", 1), 1),
        },

        # nobody on, 2 out
        ("a", 2): {
            "O": (("a", 3), 0),
            "P": (("a", 3), 0),
            "K": (("a", 3), 0),
            "W": (("b", 2), 0),
            "S": (("b", 2), 0),
            "D": (("c", 2), 0),
            "T": (("d", 2), 0),
            "H": (("a", 2), 1),
        },

        # runner on first, nobody out
        ("b", 0): {
            "O": (("b", 1), 0),
            "P": (("b", 1), 0),
            "K": (("b", 1), 0),
            "W": (("e", 0), 0),
            "S": (("e", 0), 0),
            "D": (("c", 0), 1),
            "T": (("d", 0), 1),
            "H": (("a", 0), 2),
        },

        # runner on first, one out
        ("b", 1): {
            "O": (("b", 2), 0),
            "P": (("b", 2), 0),
            "K": (("b", 2), 0),
            "W": (("e", 1), 0),
            "S": (("e", 1), 0),
            "D": (("c", 1), 1),
            "T": (("d", 1), 1),
            "H": (("a", 1), 2),
        },

        # runner on first, two outs
        ("b", 2): {
            "O": (("b", 3), 0),
            "P": (("b", 3), 0),
            "K": (("b", 3), 0),
            "W": (("e", 2), 0),
            "S": (("e", 2), 0),
            "D": (("c", 2), 1),
            "T": (("d", 2), 1),
            "H": (("a", 2), 2),
        },

        # runner on second, nobody out
        ("c", 0): {
            "O": (("c", 1), 0),
            "P": (("c", 1), 0),
            "K": (("c", 1), 0),
            "W": (("e", 0), 0),
            "S": (("b", 0), 1),
            "D": (("c", 0), 1),
            "T": (("d", 0), 1),
            "H": (("a", 0), 2),
        },

        # runner on second, one out
        ("c", 1): {
            "O": (("c", 2), 0),
            "P": (("c", 2), 0),
            "K": (("c", 2), 0),
            "W": (("e", 1), 0),
            "S": (("b", 1), 1),
            "D": (("c", 1), 1),
            "T": (("d", 1), 1),
            "H": (("a", 1), 2),
        },

        # runner on second, two outs
        ("c", 2): {
            "O": (("c", 3), 0),
            "P": (("c", 3), 0),
            "K": (("c", 3), 0),
            "W": (("e", 2), 0),
            "S": (("b", 2), 1),
            "D": (("c", 2), 1),
            "T": (("d", 2), 1),
            "H": (("a", 2), 2),
        },

        # runner on third, nobody out
        ("d", 0): {
            "O": (("d", 1), 0),
            "P": (("a", 1), 1),
            "K": (("d", 1), 0),
            "W": (("f", 0), 0),
            "S": (("b", 0), 1),
            "D": (("c", 0), 1),
            "T": (("d", 0), 1),
            "H": (("a", 0), 2),
        },

        # runner on third, one out
        ("d", 1): {
            "O": (("d", 2), 0),
            "P": (("a", 2), 1),
            "K": (("d", 2), 0),
            "W": (("f", 1), 0),
            "S": (("b", 1), 1),
            "D": (("c", 1), 1),
            "T": (("d", 1), 1),
            "H": (("a", 1), 2),
        },


        # runner on third, two outs
        ("d", 2): {
            "O": (("d", 3), 0),
            "P": (("a", 3), 0),
            "K": (("d", 3), 0),
            "W": (("f", 2), 0),
            "S": (("b", 2), 1),
            "D": (("c", 2), 1),
            "T": (("d", 2), 1),
            "H": (("a", 2), 2),
        },

        # runners on first and second, nobody out
        ("e", 0): {
            "O": (("e", 1), 0),
            "P": (("e", 1), 0),
            "K": (("e", 1), 0),
            "W": (("h", 0), 0),
            "S": (("e", 0), 1),
            "D": (("c", 0), 2),
            "T": (("d", 0), 2),
            "H": (("a", 0), 3),
        },

        # runners on first and second, one out
        ("e", 1): {
            "O": (("e", 2), 0),
            "P": (("e", 2), 0),
            "K": (("e", 2), 0),
            "W": (("h", 1), 0),
            "S": (("e", 1), 1),
            "D": (("c", 1), 2),
            "T": (("d", 1), 2),
            "H": (("a", 1), 3),
        },

        # runners on first and second, two outs
        ("e", 2): {
            "O": (("e", 3), 0),
            "P": (("e", 3), 0),
            "K": (("e", 3), 0),
            "W": (("h", 2), 0),
            "S": (("e", 2), 1),
            "D": (("c", 2), 2),
            "T": (("d", 2), 2),
            "H": (("a", 2), 3),
        },

        # runners on first and third, nobody out
        ("f", 0): {
            "O": (("f", 1), 0),
            "P": (("b", 1), 1),
            "K": (("f", 1), 0),
            "W": (("h", 0), 0),
            "S": (("e", 0), 1),
            "D": (("c", 0), 2),
            "T": (("d", 0), 2),
            "H": (("a", 0), 3),
        },

        # runners on first and third, one out
        ("f", 1): {
            "O": (("f", 2), 0),
            "P": (("b", 2), 1),
            "K": (("f", 2), 0),
            "W": (("h", 1), 0),
            "S": (("e", 1), 1),
            "D": (("c", 1), 2),
            "T": (("d", 1), 2),
            "H": (("a", 1), 3),
        },

        # runners on first and third, two outs
        ("f", 2): {
            "O": (("f", 3), 0),
            "P": (("b", 3), 0),
            "K": (("f", 3), 0),
            "W": (("h", 2), 0),
            "S": (("e", 2), 1),
            "D": (("c", 2), 2),
            "T": (("d", 2), 2),
            "H": (("a", 2), 3),
        },


        # runners on second and third, nobody out
        ("g", 0): {
            "O": (("g", 1), 0),
            "P": (("c", 1), 1),
            "K": (("g", 1), 0),
            "W": (("h", 0), 0),
            "S": (("b", 0), 2),
            "D": (("c", 0), 2),
            "T": (("d", 0), 2),
            "H": (("a", 0), 3),
        },

        # runners on second and third, one out
        ("g", 1): {
            "O": (("g", 2), 0),
            "P": (("c", 2), 1),
            "K": (("g", 2), 0),
            "W": (("h", 1), 0),
            "S": (("b", 1), 2),
            "D": (("c", 1), 2),
            "T": (("d", 1), 2),
            "H": (("a", 1), 3),
        },

        # runners on second and third, two outs
        ("g", 2): {
            "O": (("g", 3), 0),
            "P": (("c", 3), 0),
            "K": (("g", 3), 0),
            "W": (("h", 2), 0),
            "S": (("b", 2), 2),
            "D": (("c", 2), 2),
            "T": (("d", 2), 2),
            "H": (("a", 2), 3),
        },

        # bases loaded, nobody out
        ("h", 0): {
            "O": (("h", 1), 0),
            "P": (("e", 1), 1),
            "K": (("h", 1), 0),
            "W": (("h", 0), 1),
            "S": (("e", 0), 2),
            "D": (("c", 0), 3),
            "T": (("d", 0), 3),
            "H": (("a", 0), 4),
        },

        # bases loaded, one out
        ("h", 1): {
            "O": (("h", 2), 0),
            "P": (("e", 2), 1),
            "K": (("h", 2), 0),
            "W": (("h", 1), 1),
            "S": (("e", 1), 2),
            "D": (("c", 1), 3),
            "T": (("d", 1), 3),
            "H": (("a", 1), 4),
        },

        # bases loaded, two outs
        ("h", 2): {
            "O": (("h", 3), 0),
            "P": (("e", 3), 0),
            "K": (("h", 3), 0),
            "W": (("h", 2), 1),
            "S": (("e", 2), 2),
            "D": (("c", 2), 3),
            "T": (("d", 2), 3),
            "H": (("a", 2), 4),
        },
    }

    return result_dictionary[state][action]

def action_cost(state, action, new_state):
    return 0


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
    # probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6789, "P": 0}
    initial = ("a", 0)
    problem = search.Problem(initial, 10e-8, result, actions, action_cost, probabilities)

    # soln = search.get_run_expectancy(problem)
    # print(soln)

    # prob_dic = search.get_probabilities(problem)
    # print(prob_dic)

    re24_matrix = get_re24_matrix(problem)
    print(re24_matrix)