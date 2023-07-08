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
        self.grid = [[Number(random.randint(1, 9),a,b) for a in range(self.grid_size)] for b in range(self.grid_size)]

    def select_numbers(self):
        first_check = True
        while first_check:
            row = int(input(f"Enter the row (0-{self.grid_size-1}) for your selection: "))
            column = int(input(f"Enter the column (0-{self.grid_size-1}) for your selection: "))
            number = self.grid[row][column]
            if number.selected:
                print("Selected position is empty. Try again.")
            else:
                first_check = False
        selection_type = input("Enter '1' to select one number or '2' to select two numbers: ")
        number.selectNumber()
        if selection_type == "1":
            operation = input(f"Enter an operation from [+,-,*,/]")
            self.perform_operation_single(number, operation)
        else:
            flag = True
            while flag:
                row = int(input(f"Enter the row (0-{self.grid_size-1}) for your selection: "))
                column = int(input(f"Enter the column (0-{self.grid_size-1}) for your selection: "))
                number2 = self.grid[row][column]
                if not number2.selected:
                    operation = input(f"Enter an operation from [+,-,*,/]")
                    self.perform_operation(number, number2, operation)
                    number2.selectNumber()
                    flag = False
                else:
                    print("Try again, that is an empty square")

    def takeTurn(self):
        self.select_numbers()
        self.switch_players()


    def check_adjacency(self, num1, num2):

        if abs(num1.row-num2.row) > 1 or abs(num1.col-num2.col) > 1 or num2.selected:
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
                    #for now this will default to addition, fix later
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
                    #for now this will default to addition, fix later
                    self.player2_score += num1.number
                else:
                    self.player2_score /= num1.score
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
                    #for now this will default to addition, fix later
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
                    #for now this will default to addition, fix later
                    self.player2_score += num1.number + num2.number
                else:
                    self.player2_score += num1.number / num2.number
    def switch_players(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_win_condition(self):
        if self.player1_score == self.target_score:
            return 1
        elif self.player2_score == self.target_score:
            return 2
        return None
    

# Example usage
game = MathemagixGame(4)
game.start_new_round()
print("Target Score:", game.target_score)

while True:
    # Display the grid with numbers
    print("Grid:")
    for row in game.grid:
        for number in row:
            print(number, end=" ")
        print()

    print("Player 1 Score:", game.player1_score)
    print("Player 2 Score:", game.player2_score)



    game.takeTurn()

    winner = game.check_win_condition()
    if winner:
        print("Final Score:")
        print("Player 1 Score:", game.player1_score)
        print("Player 2 Score:", game.player2_score)
        print("Player", winner, "wins!")
        break

    print()
