import tkinter as tk
from tkinter import messagebox

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def minmax(board, depth, is_maximizing):
    if check_winner(board, "X"):
        return -10 + depth
    elif check_winner(board, "O"):
        return 10 - depth
    elif is_draw(board):
        return 0

    if is_maximizing:
        max_eval = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    eval = minmax(board, depth + 1, False)
                    board[row][col] = " "
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    eval = minmax(board, depth + 1, True)
                    board[row][col] = " "
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_eval = -float("inf")
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                eval = minmax(board, 0, False)
                board[row][col] = " "
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)

    return best_move

def make_move(row, col):
    global board, player_turn

    if board[row][col] == " " and player_turn:
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")
        player_turn = not player_turn

        if check_winner(board, "X"):
            end_game("Human wins!")
        elif is_draw(board):
            end_game("It's a draw!")
        else:
            bot_row, bot_col = best_move(board)
            board[bot_row][bot_col] = "O"
            buttons[bot_row][bot_col].config(text="O", state="disabled")
            player_turn = not player_turn

            if check_winner(board, "O"):
                end_game("Bot wins!")
            elif is_draw(board):
                end_game("It's a draw!")

def end_game(message):
    global player_turn
    player_turn = False
    messagebox.showinfo("Game Over", message)
    reset_board()

def reset_board():
    global board, player_turn
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_turn = True
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state="normal")

def main():
    global buttons, board, player_turn

    window = tk.Tk()
    window.title("Tic-Tac-Toe")

    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Game", command=reset_board)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)

    board = [[" " for _ in range(3)] for _ in range(3)]
    player_turn = True

    buttons = []
    for row in range(3):
        row_buttons = []
        for col in range(3):
            button = tk.Button(window, text=" ", font=("Helvetica", 24), width=5, height=2,
                               command=lambda r=row, c=col: make_move(r, c))
            button.grid(row=row, column=col, padx=5, pady=5)
            row_buttons.append(button)
        buttons.append(row_buttons)

    window.mainloop()

if __name__ == "__main__":
    main()
