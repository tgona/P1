import random
import hashlib
import numpy as np

class Number:
    def __init__(self, value, row, col):
        self.value = value
        self.number = value
        self.selected = False
        self.row = row
        self.col = col

    def selectNumber(self):
        self.selected = True
        self.value = None

    def __str__(self):
        return str(self.value)


class MathemagixGame:
    def __init__(self, grid_size, agent_player):
        self.target_score = 0
        self.player1_score = 0
        self.player2_score = 0
        self.grid = []
        self.grid_size = grid_size
        self.current_player = 1
        self.state = None
        self.agent_player = agent_player
        self.turns_taken = 0
        self.gridValues = []

    def start_new_round(self):
        self.player1_score = 0
        self.player2_score = 0
        self.generate_grid()
        self.target_score = random.randint(100, 250)
        self.update_state()

    def generate_grid(self):
        self.grid = [[Number(random.randint(1, 9), a, b) for a in range(self.grid_size)] for b in range(self.grid_size)]
        self.updateGrid()

    def select_numbers(self, action):
        if isinstance(action, int):
            print("Invalid action format. Expected list or tuple, received integer.")
            return

        first_number = action[1], action[2]
        self.grid[first_number[0]][first_number[1]].selectNumber()

        if len(action) > 3:
            second_number = action[3], action[4]
            self.grid[second_number[0]][second_number[1]].selectNumber()

        operation = action[0]
        if len(action) == 3:
            self.perform_operation_single(self.grid[first_number[0]][first_number[1]], operation)
        else:
            self.perform_operation(
                self.grid[first_number[0]][first_number[1]],
                self.grid[second_number[0]][second_number[1]],
                operation
            )
        self.update_state()
        self.turns_taken += 1
    def update_state(self):
        player_score = self.player1_score if self.current_player == 1 else self.player2_score
        opponent_score = self.player2_score if self.current_player == 1 else self.player1_score
        hashed_state = self.hash_state()
        self.state = [player_score, opponent_score, self.target_score, self.grid_size, self.agent_player, self.turns_taken, hashed_state]

    def computer_move(self):
        self.select_numbers(self.randomMoveSelector())
        if self.check_win_condition():
            self.step([],True)

    def step(self, action, turn = False):
        if not turn:
            self.select_numbers(action)

            done = self.check_win_condition()
            reward = 0
            penalty = -0.05

            if done:
                if self.current_player == 1 and self.player1_score == self.target_score:
                    reward = 1
                elif self.current_player == 2 and self.player2_score == self.target_score:
                    reward = 1

            reward += penalty
        else:
            done = True
            reward = -1
        return self.state, reward, done

    def check_adjacency(self, num1, num2):
        if abs(num1.row - num2.row) > 1 or abs(num1.col - num2.col) > 1 or num2.selected:
            return False
        return True

    def perform_operation_single(self, num1, operation):
        if self.current_player == 1:
            if operation == "+":
                self.player1_score += num1.number
            elif operation == "-":
                self.player1_score -= num1.number
            elif operation == "*":
                self.player1_score *= num1.number
            else:
                if self.player1_score % num1.number != 0:
                    self.player1_score += num1.number
                else:
                    self.player1_score /= num1.number
        else:
            if operation == "+":
                self.player2_score += num1.number
            elif operation == "-":
                self.player2_score -= num1.number
            elif operation == "*":
                self.player2_score *= num1.number
            else:
                if self.player2_score % num1.number != 0:
                    self.player2_score += num1.number
                else:
                    self.player2_score /= num1.number

    def perform_operation(self, num1, num2, operation):
        if self.current_player == 1:
            if operation == "+":
                self.player1_score += num1.number + num2.number
            elif operation == "-":
                self.player1_score += num1.number - num2.number
            elif operation == "*":
                self.player1_score += num1.number * num2.number
            else:
                if num1.value % num2.value != 0:
                    self.player1_score += num1.number + num2.number
                else:
                    self.player1_score += num1.number / num2.number
        else:
            if operation == "+":
                self.player2_score += num1.number + num2.number
            elif operation == "-":
                self.player2_score += num1.number - num2.number
            elif operation == "*":
                self.player2_score += num1.number * num2.number
            else:
                if num1.value % num2.value != 0:
                    self.player2_score += num1.number + num2.number
                else:
                    self.player2_score += num1.number / num2.number

    def get_legal_moves(self):
        legal_moves = []

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                number = self.grid[row][col]

                if not number.selected:
                    legal_moves.append(["+", row, col])
                    legal_moves.append(["-", row, col])
                    legal_moves.append(["x", row, col])
                    if self.current_player == 1:
                        if not self.player1_score % number.number:
                            legal_moves.append(["/", row, col])
                    for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        adj_row = row + direction[0]
                        adj_col = col + direction[1]

                        if 0 <= adj_row < self.grid_size and 0 <= adj_col < self.grid_size:
                            adj_number = self.grid[adj_row][adj_col]
                            if not adj_number.selected:
                                legal_moves.append(["+", row, col, adj_row, adj_col])
                                legal_moves.append(["-", row, col, adj_row, adj_col])
                                legal_moves.append(["x", row, col, adj_row, adj_col])
                            if not adj_number.selected and not adj_number.number % number.number:
                                legal_moves.append(["/", row, col, adj_row, adj_col])

        return legal_moves

    def hash_state(self):
        return self.gridValues

    def updateGrid(self):
        self.gridValues = [[self.grid[a][b].value for a in range(len(self.grid))] for b in range(len(self.grid))]

    def randomMoveSelector(self):
        possible_moves = self.get_legal_moves()
        return possible_moves[random.randrange(len(possible_moves))]

    def check_win_condition(self):
        if self.current_player == 1 and self.player1_score == self.target_score:
            return True
        elif self.current_player == 2 and self.player2_score == self.target_score:
            return True
        return False

    def reset(self):
        self.start_new_round()
        return self.state
