# Greedy Agent for Hoot Owl Hoot
import sys
import random

board = ["yellow", "green", "orange", "blue", "purple", "red", "blue", "purple", 
         "red", "yellow", "green", "blue", "orange", "red", "purple", "yellow", 
         "green", "orange", "blue", "purple", "red", "green", "yellow", "orange", 
         "blue", "purple", "red", "yellow", "green", "blue", "orange", "red", 
         "purple", "yellow", "green", "blue", "orange", "red", "purple", "nest"]

cards = ["blue", "purple", "red", "yellow", "green", "orange", "sun"]

board_len = len(board)
sun_len = 14

card_probabilities = {
    "blue": 0.12,
    "purple": 0.12,
    "red": 0.12,
    "yellow": 0.12,
    "green": 0.12,
    "orange": 0.12,
    "sun": 0.28
}

def is_terminal(state):
    # Checks that either the sun has reached the end or all owls are at the end
    return state[-1] == sun_len - 1 or all([pos == board_len - 1 for pos in state[:-1]])


def get_best_action(state, set_cards):
    # Returns the best action we can take given the current state and the cards
    best_action = None
    best_progress = float("-inf")
    best_owl = None

    if "sun" in set_cards:
        next_sun = state[-1] + 1
        new_state = list(state[:-1] + [next_sun])
        best_action = "sun"
        best_owl = None
        best_state = new_state
        return best_progress, best_action, best_owl, best_state

    for card in set_cards:
        owls = state[:-1]
        for i in range(len(state) - 1):
            if state[i] == board_len - 1:
                continue
            for j in range(state[i] + 1, board_len):
                if board[j] == "nest":
                    next_pos = j
                    break
                elif board[j] == card and j not in owls:
                    next_pos = j
                    break
            new_state = list(state)
            new_state[i] = next_pos
            # Calculate forward progress made from this move and compare to best progress
            progress = next_pos - state[i]
            if progress > best_progress:
                best_progress = progress
                best_action = card
                best_owl = i
                best_state = new_state
    return best_progress, best_action, best_owl, best_state
    

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: ./Greedy <state> <num_games> or ./Greedy <state> <card1,card2,card3>")
        exit(0)
    
    state = sys.argv[1]
    state = state.split(",")
    state = [int(x) for x in state]

    # Error checking
    owl_pos = state[:-1]
    sun_pos = state[-1]
    if sun_pos < 0 or sun_pos >= sun_len:
        print("Invalid sun position inputted. Sun position should be between 0 and 13.")
        exit(1)
    for pos in owl_pos:
        if pos < 0 or pos >= board_len:
            print("Invalid owl position inputted. Owl positions should be between 0 and 39.")
            exit(1)
        # Check if two owl positions are the same
        if owl_pos.count(pos) > 1 and pos != 39:
            print("Invalid owl positions inputted. Owl positions should be unique.")
            exit(1)
    if len(state) < 4 or len(state) > 7:
        print("Invalid state inputted. States should consist of 3-6 owl positions and the sun position.")
        exit(1)

    # Evaluation
    if sys.argv[2].isdigit():
        num_games = int(sys.argv[2])
        # Simulate running the game num_games times, choosing best action every time
        # and outputting the average win probability
        wins = 0
        start_state = state
        for _ in range(num_games):
            # Always start from beginning
            probabilities = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.28]
            state = start_state
            # Pick 3 random cards
            random_cards = random.choices(cards, probabilities, k=3)
            while not is_terminal(state):
                best_prob, best_action, best_owl, best_state = get_best_action(state, random_cards)
                state = best_state
                # Remove the card we played from our set and add a new random card
                random_cards.remove(best_action)
                random_cards.append(random.choices(cards, probabilities)[0])
            if state[-1] == sun_len - 1:
                wins += 0
            else:
                wins += 1
        print("Average Win Percentage: " + str(wins / num_games * 100) + "%")
        return

    set_cards = sys.argv[2]
    set_cards = set_cards.split(",")
    if len(set_cards) != 3:
        print("Invalid number of cards inputted. Please input 3 cards.")
        exit(1)
    for card in set_cards:
        if card not in cards:
            print("Invalid card inputted. Please input a valid card.")
            exit(1)
    if is_terminal(state):
        print("Inputted state is terminal; no action possible")
        exit(0)
    if "sun" in set_cards:
        print("Sun card in hand; you must play it")
        exit(0)
    best_prob, best_action, best_owl, best_state = get_best_action(state, set_cards)
    print("Best action to take is to move owl " + str(best_owl + 1) + 
            " using card " + best_action + ", resulting in position " + 
            str(best_state) + " with forward progress of " + str(best_prob))


if __name__ == "__main__":
    main()
