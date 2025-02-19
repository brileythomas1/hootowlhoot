# MCTS Agent for Hoot Owl Hoot
import sys
import math
import random

board = ["yellow", "green", "orange", "blue", "purple", "red", "blue", "purple", 
         "red", "yellow", "green", "blue", "orange", "red", "purple", "yellow", 
         "green", "orange", "blue", "purple", "red", "green", "yellow", "orange", 
         "blue", "purple", "red", "yellow", "green", "blue", "orange", "red", 
         "purple", "yellow", "green", "blue", "orange", "red", "purple", "nest"]

cards = ["blue", "purple", "red", "yellow", "green", "orange", "sun"]

board_len = len(board)
sun_len = 14

# Uniform probability distribution based on real deck.
# Six cards of each color and 14 sun cards.
card_probabilities = {
    "blue": 0.12,
    "purple": 0.12,
    "red": 0.12,
    "yellow": 0.12,
    "green": 0.12,
    "orange": 0.12,
    "sun": 0.28
}

visited = {}

def is_terminal(state):
    # Checks that either the sun has reached the end or all owls are at the end
    return state[-1] == sun_len - 1 or all([pos == board_len - 1 for pos in state[:-1]])

# Get all possible actions given the current state
def get_actions(state):
    # Returns all the possible actions we can take given the current state
    actions = []
    # For each card
    for card in cards:
        # For each owl
        for i in range(len(state) - 1):
            # Skip owls at nest
            if state[i] == board_len - 1:
                continue
            # Find the next position we can move to with the card and save it in actions
            for j in range(state[i] + 1, board_len):
                if board[j] == card or board[j] == "nest":
                    actions.append((card, i, j))
                    break
    actions.append(("sun", None, None))
    return actions

# Get the next state given the a state and the action to make in that state
def successor(state, action):
    if action[0] == "sun":
        new_state = list(state)
        new_state[-1] += 1
        return tuple(new_state)

    card, owl, next_pos = action
    new_state = list(state)
    new_state[owl] = next_pos
    return tuple(new_state)

def monte_carlo(root):
    def traverse(state):
        # UCB formula to balance exploration and exploitation
        def ucb(parent, children):
            parent_visits = visited[tuple(parent)][1]
            return max(children, key=lambda node: (visited[tuple(node)][0] / visited[tuple(node)][1]) + (math.sqrt(2 * math.log(parent_visits) / visited[tuple(node)][1])))
    

        children = [successor(state, move) for move in get_actions(state) if successor(state, move) in visited]
        # While not terminal and all children have been visited, keep traversing down
        while not is_terminal(state) and len(children) == len(get_actions(state)):
            state = ucb(state, children)
            children = [successor(state, move) for move in get_actions(state) if successor(state, move) in visited]
            path.append(tuple(state))
        return state

    def expand(state):
        children = [successor(state, move) for move in get_actions(state) if successor(state, move) not in visited]
        child = random.choice(children)
        # Expand leaves by adding them to visited
        visited[child] = (0, 0)
        path.append(child)
        return child
    
    def simulate(state):
        # Simulate playouts until terminal state
        while not is_terminal(state):
            state = successor(state, random.choice(get_actions(state)))
        return 1 if state[-1] != sun_len - 1 else 0
    
    def update(reward):
        # Update the value of each state in the path
        # In a difference from Pset 4, we don't have to consider rewards from
        # a particular player's perspective, as the game is cooperative
        for state in path:
            value, visits = visited[tuple(state)]
            value += reward
            visited[tuple(state)] = (value, visits + 1)
    
    path = [root]
    s_prime = traverse(root)
    if not is_terminal(s_prime):
        child = expand(s_prime)
        reward = simulate(child)
    else:
        reward = 1 if s_prime[-1] != sun_len - 1 else 0
    update(reward)
    

def main():
    if len(sys.argv) != 4:
        print("Usage: ./MCTS <state> <iterations> <cards>")
        sys.exit(0)
    
    iterations = int(sys.argv[2])
    state = sys.argv[1].split(",")
    state = [int(x) for x in state]
    visited[tuple(state)] = (0, 0)
    
    for _ in range(iterations):
        monte_carlo(state)
    
    set_cards = sys.argv[3].split(",")
    best_action = None
    best_state = None
    best_value = float("-inf")
    for card in set_cards:
        owls = state[:-1]
        for i in range(len(owls)):
            for j in range(state[i] + 1, board_len):
                if board[j] == "nest":
                    next_pos = j
                    break
                elif board[j] == card and j not in owls:
                    next_pos = j
                    break
            new_state = list(state)
            new_state[i] = next_pos
            if visited.get(tuple(new_state), (0, 0))[1] > 0 and visited[tuple(new_state)][1] > best_value:
                best_value = visited[tuple(new_state)][1]
                best_action = (card, i, j)
                best_state = new_state
    if best_action:
        print("Best action to take is to move owl " + str(best_action[1] + 1) + 
        " using card " + best_action[0] + ", resulting in position " + 
        str(best_state) + " with " + str(best_value) + " visits")
    else:
        print("Please run with more iterations.")

    
if __name__ == "__main__":
    main()