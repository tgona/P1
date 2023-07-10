import random
import tkinter as tk


class Number:
    def __init__(self, value, row, col):
        self.value = value
        self.number = value
        self.selected = False
        self.row = row
        self.col = col

    def selectNumber(self):
        self.selected = not self.selected
        self.value = None if self.selected else self.number

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
        self.root = tk.Tk()
        self.buttons = []
        self.selected_numbers = []
        self.operation_buttons = []

        self.start_new_round()

    def start_new_round(self):
        self.player1_score = 0
        self.player2_score = 0
        self.generate_grid()
        self.target_score = random.randint(50, 100)
        self.create_gui()

    def generate_grid(self):
        self.grid = [[Number(random.randint(1, 9), a, b) for a in range(self.grid_size)] for b in
                     range(self.grid_size)]

    def create_gui(self):
        self.root.title("Mathemagix Game")

        grid_frame = tk.Frame(self.root)
        grid_frame.pack(side=tk.LEFT)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                number = self.grid[row][col]
                button = tk.Button(grid_frame, text=str(number), width=5, height=2,
                                   command=lambda r=row, c=col: self.select_number(r, c))
                button.grid(row=row, column=col)
                self.buttons.append(button)

        operations_frame = tk.Frame(self.root)
        operations_frame.pack(side=tk.RIGHT, padx=10)

        operation_labels = ["+", "-", "*", "/"]
        for label in operation_labels:
            button = tk.Button(operations_frame, text=label, width=5, height=2,
                               command=lambda op=label: self.set_operation(op))
            button.pack(pady=5)
            self.operation_buttons.append(button)

        self.update_scores()

    def select_number(self, row, col):
        number = self.grid[row][col]

        if number.selected:
            number.unselectNumber()
            self.buttons[row * self.grid_size + col].config(relief=tk.RAISED)
            self.selected_numbers.remove(number)
        else:
            if len(self.selected_numbers) < 2:
                number.selectNumber()
                self.buttons[row * self.grid_size + col].config(relief=tk.SUNKEN)
                self.selected_numbers.append(number)

                if len(self.selected_numbers) == 2:
                    self.perform_operation()

        self.switch_players()
        self.update_scores()

    def perform_operation(self):
        number1, number2 = self.selected_numbers

        if self.current_player == 1:
            player_score = self.player1_score
        else:
            player_score = self.player2_score

        if number1.number % number2.number == 0:
            operation = "/"
        else:
            operation = "+"

        if operation == "+":
            player_score += number1.number + number2.number
        else:
            player_score //= number2.number

        if self.current_player == 1:
            self.player1_score = player_score
        else:
            self.player2_score = player_score

    def set_operation(self, operation):
        self.operation_buttons[0].config(relief=tk.RAISED)
        self.operation_buttons[1].config(relief=tk.RAISED)
        self.operation_buttons[2].config(relief=tk.RAISED)
        self.operation_buttons[3].config(relief=tk.RAISED)

        if operation == "+":
            self.operation_buttons[0].config(relief=tk.SUNKEN)
        elif operation == "-":
            self.operation_buttons[1].config(relief=tk.SUNKEN)
        elif operation == "*":
            self.operation_buttons[2].config(relief=tk.SUNKEN)
        elif operation == "/":
            self.operation_buttons[3].config(relief=tk.SUNKEN)

    def switch_players(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def update_scores(self):
        self.root.title(f"Mathemagix Game | Player 1 Score: {self.player1_score} | Player 2 Score: {self.player2_score}")

    def check_win_condition(self):
        if self.player1_score == self.target_score:
            return 1
        elif self.player2_score == self.target_score:
            return 2
        return None

    def get_legal_moves(self):
        legal_moves = []

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                number = self.grid[row][col]

                if not number.selected:
                    for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        adj_row = row + direction[0]
                        adj_col = col + direction[1]

                        if 0 <= adj_row < self.grid_size and 0 <= adj_col < self.grid_size:
                            adj_number = self.grid[adj_row][adj_col]

                            if adj_number.selected and not adj_number.value % number.value:
                                legal_moves.append(["[operation, row, col]", row, col, adj_row, adj_col])

        return legal_moves

    def run(self):
        self.root.mainloop()


# Example usage
game = MathemagixGame(4)
game.run()
