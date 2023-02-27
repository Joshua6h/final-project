from argparse import _ActionsContainer
from collections import deque
import math
from unittest import result

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return  f"Node({self.state})"

    def __len__(self):
        if self.parent is None:
            return 0
        else:
            return len(self.parent) + 1

    def __lt__(self, other):
        return self.path_cost < other.path_cost

failure = Node('failure', path_cost=math.inf)
cutoff = Node('cutoff', path_cost=math.inf)

class Problem:
    def __init__(self, initial, min_prob, result, actions, action_cost, probabilities):
        self.initial = initial
        self.min_prob = min_prob
        self.result = result
        self.actions = actions
        self.action_cost = action_cost
        self.probabilities = probabilities


def extract_path(node):
    if node is None:
        return []
    else:
        return extract_path(node.parent) + [node.state]

def expand(problem, node):
    state = node.state
    for action in problem.actions(state):
        new_state = problem.result(state, action)
        cost = node.path_cost + problem.action_cost(state, action, new_state)
        yield Node(state=new_state, parent=node, action=action, path_cost=cost)


def get_run_expectancy(problem):
    node = (Node(problem.initial), 1)
    total_runs = 0
    if node[1] < problem.min_prob or node[0].state[1] >= 3:
        return total_runs
    
    frontier = deque([(node[0], 1)])

    total_prob = 0

    while frontier:
        node = frontier.pop()
        for child in expand(problem, node[0]):
            # need to increment total runs for each node
            if (child.action == "P" or child.action == "K") and node[1] * problem.probabilities[child.action] * child.state[1] > 0:
                s = 2
            total_runs += node[1] * problem.probabilities[child.action] * child.state[1]
            s = (child.state, node[1] * problem.probabilities[child.action])
            # if s[1] < child.action_cost:
            #     return total_runs

            if child.state[0][1] < 3 and (child.state[0][0] == "d" or child.state[0][0] == "f" or child.state[0][0] == "g" or child.state[0][0] == "h"):
                total_prob += s[1]
                
            if s[1] > problem.min_prob and child.state[0][1] < 3:
                child.state = child.state[0]
                frontier.appendleft((child, s[1]))
            

    print("Total Prob: " + str(total_prob))
    return total_runs

