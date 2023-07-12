from game import MathemagixGame
import random
# Example usage
game = MathemagixGame(4)
game.start_new_round()
print("Target Score:", game.target_score)
game.mode = "comp"
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
    print(available_moves)
    #Replace below line with agents method to get next move
    selected_move = available_moves[random.randrange(len(available_moves))]
    game.takeTurn(selected_move)
    turns += 1
    winner = game.check_win_condition()
    if winner:
        print("Final Score:")
        print("Player 1 Score:", game.player1_score)
        print("Player 2 Score:", game.player2_score)
        print("Player", winner, "wins!")
        break

    print()
print(f"Turns: {turns}")
