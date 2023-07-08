import tkinter as tk
from engine import MathemagixGame


class MathemagixGUI:
    def __init__(self, grid_size):
        self.game = MathemagixGame(grid_size)

        self.root = tk.Tk()
        self.root.title("Mathemagix")

        self.number_buttons = []

        self.create_number_buttons()
        self.create_score_labels()

        self.game.start_new_round()

    def create_number_buttons(self):
        for row in range(self.game.grid_size):
            row_buttons = []
            for col in range(self.game.grid_size):
                number = self.game.grid[row][col]
                button = tk.Button(
                    self.root, text=number.value, width=4, height=2,
                    command=lambda r=row, c=col: self.button_click(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.number_buttons.append(row_buttons)

    def create_score_labels(self):
        player1_label = tk.Label(self.root, text="Player 1 Score:")
        player1_label.grid(row=self.game.grid_size, column=0, pady=10)

        player1_score = tk.Label(self.root, textvariable=self.game.player1_score)
        player1_score.grid(row=self.game.grid_size, column=1, pady=10)

        player2_label = tk.Label(self.root, text="Player 2 Score:")
        player2_label.grid(row=self.game.grid_size, column=2, pady=10)

        player2_score = tk.Label(self.root, textvariable=self.game.player2_score)
        player2_score.grid(row=self.game.grid_size, column=3, pady=10)

    def button_click(self, row, col):
        number = self.game.grid[row][col]

        if self.game.current_player == 1:
            self.number_buttons[row][col].config(state=tk.DISABLED)
        else:
            self.number_buttons[row][col].config(state=tk.DISABLED)

        self.game.select_numbers(number)

        winner = self.game.check_win_condition()
        if winner:
            print("Final Score:")
            print("Player 1 Score:", self.game.player1_score)
            print("Player 2 Score:", self.game.player2_score)
            print("Player", winner, "wins!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = MathemagixGUI(4)
    game.run()
