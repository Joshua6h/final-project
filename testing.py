import unittest
import search
import re24

class TestSearch(unittest.TestCase):

    def test_get_probabilities(self):
        probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
        problem = search.Problem(("a", 0), 10e-8, re24.result, re24.actions, re24.action_cost, probabilities)
        state_probs = search.get_probabilities(problem)
        total_prob = 0
        for state in state_probs:
            total_prob += state_probs[state]
        self.assertEqual(total_prob, 1)


    def test_get_run_expectancy(self):
        probabilities = {"W": 0, "S": 0, "D": 0, "T": 0, "H": 0, "O": 1, "P": 0}
        problem = search.Problem(("a", 0), 10e-8, re24.result, re24.actions, re24.action_cost, probabilities)
        run_expectancy = search.get_run_expectancy(problem)
        # If all players get out, no runs are scored
        self.assertEqual(run_expectancy, 0)


        probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
        problemA = search.Problem(("a", 0), 10e-8, re24.result, re24.actions, re24.action_cost, probabilities)
        run_expectancyA = search.get_run_expectancy(problemA)

        probabilities = {"W": .0895, "S": .1556, "D": .0456, "T": .0048, "H": .0255, "O": .6648, "P": .0141}
        problemB = search.Problem(("a", 2), 10e-8, re24.result, re24.actions, re24.action_cost, probabilities)
        run_expectancyB = search.get_run_expectancy(problemB)
        # Less runs are scored after two outs than with 0 outs
        self.assertLess(run_expectancyB, run_expectancyA)


class TestRE24(unittest.TestCase):

    def test_results(self):
        result = re24.result(("b", 2), "O")
        self.assertEqual((("b", 3), 0), result)

        result = re24.result(("c", 1), "S")
        self.assertEqual((("b", 1), 1), result)


if __name__ == '__main__':
    unittest.main()