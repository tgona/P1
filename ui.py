import tkinter as tk

# Create the main window
root = tk.Tk()

# Create the header
header = tk.Frame(root)
header.pack(fill="x")

# Create the score labels
player1_score = tk.Label(header, text="Player 1: 0")
player1_score.pack(side="left")
target_score = tk.Label(header, text="Target Score: 21")
target_score.pack(side="left")
player2_score = tk.Label(header, text="Player 2: 0")
player2_score.pack(side="right")

# Create the grid
grid = tk.Frame(root)
grid.pack(fill="both", expand=True)

# Create the buttons
buttons = []
for i in range(5):
    for j in range(5):
        button = tk.Button(grid, text=str(i * 5 + j + 1), width=10, height=5)
        button.grid(row=i, column=j)
        buttons.append(button)
# Define the click handler function
def click_handler(event):
    # Get the button that was clicked
    button = event.widget

    # Update the score labels
    player1_score.config(text="Player 1: " + str(button.cget("text")))
    player2_score.config(text="Player 2: " + str(button.cget("text")))

    # Change the background color of the button to dark gray
    button.config(bg="#444444")

    # If the button is clicked again, change the background color back to normal
    if button.cget("bg") == "#444444":
        button.config(bg="white")

# Bind the click event to each button
for button in buttons:
    button.bind("<Button-1>", click_handler)

# Start the main loop
root.mainloop()