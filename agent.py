from game import MathemagixGame
import random
from stable_baselines3 import PPO

# Define the PPOAgent class
class PPOAgent:
    
def brute_force_move(game):
    legal_moves = game.get_legal_moves()
    best_move = None
    best_score = -float('inf')

    for move in legal_moves:
        # Simulate the move in a copy of the game
        game_copy = MathemagixGame(game.grid_size)
        game_copy.grid = [row[:] for row in game.grid]  # Create a deep copy of the grid
        game_copy.current_player = game.current_player
        game_copy.player1_score = game.player1_score
        game_copy.player2_score = game.player2_score

        if len(move) == 3:
            game_copy.perform_operation_single(game_copy.grid[move[1]][move[2]], move[0])
            game_copy.grid[move[1]][move[2]].selectNumber()
        else:
            game_copy.perform_operation(
                game_copy.grid[move[1]][move[2]],
                game_copy.grid[move[3]][move[4]],
                move[0]
            )
            game_copy.grid[move[1]][move[2]].selectNumber()
            game_copy.grid[move[3]][move[4]].selectNumber()

        # Evaluate the game state after the move
        score = evaluate_game_state(game_copy)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


