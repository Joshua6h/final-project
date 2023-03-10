from collections import deque

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

# returns run expectancy of a specific game state
def get_run_expectancy(problem):
    node = (Node(problem.initial), 1)
    total_runs = 0
    
    frontier = deque([(node[0], 1)])

    while frontier:
        node = frontier.pop()
        for child in expand(problem, node[0]):
            # multiply the runs scored on the action by the probability of that action occuring in that game state
            # add this to the total runs
            total_runs += node[1] * problem.probabilities[child.action] * child.state[1]
            s = (child.state, node[1] * problem.probabilities[child.action])
                
            # if the inning is not over in this state and the probability is not too low, add the new state to the frontier
            if s[1] > problem.min_prob and child.state[0][1] < 3:
                child.state = child.state[0]
                frontier.appendleft((child, s[1]))
            
    return total_runs

# return a dictionary of the relative probabilities of being in a specific game state
# probabilities must add up to 1
def get_probabilities(problem):
    node = (Node(problem.initial), 1)
    probabilities_dict = {
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
    
    frontier = deque([(node[0], 1)])

    while frontier:
        node = frontier.pop()
        for child in expand(problem, node[0]):
            if child.state[0][1] < 3:
                probabilities_dict[child.state[0]] += node[1] * problem.probabilities[child.action]
            s = (child.state, node[1] * problem.probabilities[child.action])
                
            if s[1] > problem.min_prob and child.state[0][1] < 3:
                child.state = child.state[0]
                frontier.appendleft((child, s[1]))
        
    total_prob = 0
    for item in probabilities_dict.items():
        total_prob += item[1]

    for item in probabilities_dict.items():
        probabilities_dict[item[0]] = probabilities_dict[item[0]] / total_prob

    return probabilities_dict