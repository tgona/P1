import random

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
    def __init__(self, grid_size):
        self.target_score = 0
        self.player1_score = 0
        self.player2_score = 0
        self.grid = []
        self.grid_size = grid_size
        self.current_player = 1
        self.state = None

    def switch_mode(self):
        if self.mode == "comp":
            self.mode = "text"
        else:
            self.mode = "comp"

    def start_new_round(self):
        self.player1_score = 0
        self.player2_score = 0
        self.generate_grid()
        self.target_score = random.randint(100, 250)

    def generate_grid(self):
        self.grid = [[Number(random.randint(1, 9), a, b) for a in range(self.grid_size)] for b in range(self.grid_size)]

    def select_numbers(self, action):
        first_number = action[1], action[2]
        self.grid[first_number[0]][first_number[1]].selectNumber()
        
        if len(action) > 3:
            second_number = action[3], action[4]
            self.grid[second_number[0]][second_number[1]].selectNumber()
        
        operation = action[0]
        if len(action) == 3:
            self.perform_operation_single(self.grid[first_number[0]][first_number[1]], operation)
        else:
            self.perform_operation(self.grid[first_number[0]][first_number[1]], self.grid[second_number[0]][second_number[1]], operation)

    def update_state(self):
        player_score = self.player1_score if self.current_player == 1 else self.player2_score
        opponent_score = self.player2_score if self.current_player == 1 else self.player1_score
        grid_configuration = [number.value if not number.selected else None for row in self.grid for number in row]
        self.state = [player_score, opponent_score, self.target_score, self.grid_size, grid_configuration]

    def step(self, action):
        self.select_numbers(action)
        self.update_state()

        done = self.check_win_condition()
        reward = 0
        penalty = -0.05

        if done:
            if self.current_player == 1 and self.player1_score == self.target_score:
                reward = 1
            elif self.current_player == 2 and self.player2_score == self.target_score:
                reward = 1
            else:
                reward = -1

        reward += penalty

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
    
    def check_win_condition(self):
        if self.current_player == 1 and self.player1_score == self.target_score:
            return True
        elif self.current_player == 2 and self.player2_score == self.target_score:
            return True
        return False
