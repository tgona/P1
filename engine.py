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
        self.current_player = 1
        self.grid_size = grid_size

    def start_new_round(self):
        self.player1_score = 0
        self.player2_score = 0
        self.generate_grid()
        self.target_score = random.randint(50, 100)

    def generate_grid(self):
        self.grid = [[Number(random.randint(1, 9), a, b) for a in range(self.grid_size)] for b in range(self.grid_size)]

    def select_numbers(self, number):
        if number.selected:
            print("Selected position is empty. Try again.")
            return

        number.selectNumber()

        if self.current_player == 1:
            self.player1_score += number.number
        else:
            self.player2_score += number.number

        self.switch_players()

    def perform_operation(self, number1, number2, operation):
        if self.current_player == 1:
            if operation == "+":
                self.player1_score += number1.number + number2.number
            elif operation == "-":
                self.player1_score += number1.number - number2.number
            elif operation == "*":
                self.player1_score += number1.number * number2.number
            else:
                if number1.value % number2.value != 0:
                    # For now, this will default to addition. Fix later.
                    self.player1_score += number1.number + number2.number
                else:
                    self.player1_score += number1.number / number2.number
        else:
            if operation == "+":
                self.player2_score += number1.number + number2.number
            elif operation == "-":
                self.player2_score += number1.number - number2.number
            elif operation == "*":
                self.player2_score += number1.number * number2.number
            else:
                if number1.value % number2.value != 0:
                    # For now, this will default to addition. Fix later.
                    self.player2_score += number1.number + number2.number
                else:
                    self.player2_score += number1.number / number2.number

        self.switch_players()

    def switch_players(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_win_condition(self):
        if self.player1_score == self.target_score:
            return 1
        elif self.player2_score == self.target_score:
            return 2
        return None
