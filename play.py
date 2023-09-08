import tkinter as tk
import random

# Global variables
player_turn = None
turn = None
grid_size = 3
grid = []
tk_grid = None

error = False

# Logical aspect
def initialize_grid(size):
    global grid
    grid = [[' ' for column in range(size)] for line in range(size)]

# Computer gameplay
def random_play():
    random_line = random.randint(0, grid_size-1)
    random_column = random.randint(0, grid_size-1)
    # Cell already occupied
    while grid[random_line][random_column] != " ":
        random_line = random.randint(0, grid_size - 1)
        random_column = random.randint(0, grid_size - 1)
    fill_case(random_line, random_column)

def choose_turn(symbol):
    global turn
    global player_turn
    turn = symbol
    player_turn = symbol
    initialize_grid(grid_size)
    fill_grid()
    choices_window.withdraw()
    game_window.deiconify()

def reset_game():
    global grid
    global turn
    for line in range(grid_size):
        for column in range(grid_size):
            # 'Backend' grid
            grid[line][column] = ' '
            # 'Frontend' grid
            tk_grid[line][column].config(text=' ')
    turn = player_turn
    choices_window.deiconify()
    game_window.withdraw()
    o_winner_window.withdraw()
    x_winner_window.withdraw()
    eq_window.withdraw()

def fill_grid():
    global tk_grid
    tk_grid = [[None for column in range(grid_size)] for line in range(grid_size)]

    game_frame = tk.Frame(game_window, padx=10, pady=10)
    game_frame.grid(row=1, column=0)

    for line in range(grid_size):
        for column in range(grid_size):
            tk_grid[line][column] = tk.Button(game_frame, text=" ", width=5, height=2, command=lambda line=line, column=column: fill_case(line, column))
            tk_grid[line][column].grid(row=line, column=column)

def is_completed_grid(grid):
    for line in grid:
        for column in line:
            if column == " ":
                return False
    return True

def check_end_game():
    # Checks for winner
    for line in range(grid_size):
        # Horizontal check
        symbol = grid[line][0]
        if symbol != " " and all(grid[line][column] == symbol for column in range(1, grid_size)):
            return symbol

        # Vertical check
        symbol = grid[0][line]
        if symbol != " " and all(grid[column][line] == symbol for column in range(1, grid_size)):
            return symbol

    # Diagonal check (left to right)
    symbol = grid[0][0]
    if symbol != " " and all(grid[i][i] == symbol for i in range(1, grid_size)):
        return symbol

    # Diagonal check (right to left)
    symbol = grid[0][grid_size - 1]
    if symbol != " " and all(grid[i][grid_size - 1 - i] == symbol for i in range(1, grid_size)):
        return symbol

    # Checks if completed grid
    if is_completed_grid(grid):
        return "égalité"

    return None


def fill_case(line, column):
    global turn
    # Game over
    if o_winner_window.state() == "normal" or x_winner_window.state() == "normal" or eq_window.state() == "normal":
        pass
    else:
        if grid[line][column] == " ":
            grid[line][column] = turn
            tk_grid[line][column].config(text=turn)
            if check_end_game() is not None:
                if check_end_game() == "O":
                    o_winner_window.deiconify()
                elif check_end_game() == "X":
                    x_winner_window.deiconify()
                else:
                    eq_window.deiconify()
            else:
                if turn == "O":
                    turn = "X"
                else:
                    turn = "O"
                # Not my turn -> computer's turn
                if turn != player_turn:
                    random_play()

# Check if game over before closing game window
def prevent_close():
    if o_winner_window.state() != "normal" and x_winner_window.state() != "normal" and eq_window.state() != "normal":
        game_window.withdraw()

# Visual appearance
# Choice Window
choices_window = tk.Tk()
choices_window.geometry("400x100")
choices_window.title("Choix de symbole")

pack_text = tk.Frame(choices_window)
pack_text.pack(pady=15)
text_choice = tk.Label(pack_text, text="Veuillez choisir un symbole avant de commencer")
text_choice.config(
    font=("Arial", 8, "bold")
)
text_choice.pack()
pack_tk_grid = tk.Frame(choices_window)
pack_tk_grid.pack()

bouton1 = tk.Button(pack_tk_grid, text="X", command=lambda: choose_turn("X"))
bouton2 = tk.Button(pack_tk_grid, text="O", command=lambda: choose_turn("O"))
bouton1.pack(side="left", padx=10)
bouton2.pack(side="left")

text_input = tk.Frame(choices_window)
text_input.pack(pady=15)

# O Winner window
o_winner_window = tk.Tk()
o_winner_window.title("Bravo O")
o_winner_window.geometry("380x50")
o_text = tk.Frame(o_winner_window)
o_text.pack(pady=15)
o_label = tk.Label(o_text, text="Félicitations, le joueur O a gagné ! (Fermez cette fenêtre pour relancer)")
o_label.pack()

o_winner_window.withdraw()
o_winner_window.protocol("WM_DELETE_WINDOW", reset_game)

# X Winner window
x_winner_window = tk.Tk()
x_winner_window.title("Bravo X")
x_winner_window.geometry("380x50")
x_text = tk.Frame(x_winner_window)
x_text.pack(pady=15)
x_label = tk.Label(x_text, text="Félicitations, le joueur X a gagné ! (Fermez cette fenêtre pour relancer)")
x_label.pack()

x_winner_window.withdraw()
x_winner_window.protocol("WM_DELETE_WINDOW", reset_game)

# Equality window
eq_window = tk.Tk()
eq_window.title("Égalité")
eq_window.geometry("380x50")
eq_text = tk.Frame(eq_window)
eq_text.pack(pady=15)
eq_label = tk.Label(eq_text, text="Pas de vainqueur ! (Fermez cette fenêtre pour relancer)")
eq_label.pack()

eq_window.withdraw()
eq_window.protocol("WM_DELETE_WINDOW", reset_game)

# Game Window
game_window = tk.Tk()
game_window.title("TicTacToe")
game_window.protocol("WM_DELETE_WINDOW", prevent_close)
game_window.withdraw()

game_window.mainloop()
