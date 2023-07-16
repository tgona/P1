from game import MathemagixGame
import random
import hashlib

# Example usage
game = MathemagixGame(3)
game.start_new_round()
def testBase(game):
    print("Target Score:", game.target_score)
    turns = 0
    while True:
        # Display the grid with numbers
        if not len(game.get_legal_moves()):
            game.generate_grid()
        print("Grid:")
        for row in game.grid:
            for number in row:
                print(number, end=" ")
            print()
        available_moves = game.get_legal_moves()
        print("Player 1 Score:", game.player1_score)
        print("Player 2 Score:", game.player2_score)
        #Replace below line with agents method to get next move
        if game.mode == "comp":
            selected_move = available_moves[random.randrange(len(available_moves))]
            game.takeTurn(selected_move)
            turns += 1
        else:
            game.takeTurn()
        winner = game.check_win_condition()
        if winner:
            print("Final Score:")
            print("Player 1 Score:", game.player1_score)
            print("Player 2 Score:", game.player2_score)
            print("Player", winner, "wins!")
            break

        print()
    print(f"Turns: {turns}")
def test_player():
    game.mode = 'text'

def hash_state(grid_state):
    state_str = str(grid_state)
    state_hash = hashlib.md5(state_str.encode()).hexdigest()
    return state_hash
test_player()
testBase(game)