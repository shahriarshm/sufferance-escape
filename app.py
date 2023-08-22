import os
from colorama import Fore, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    clear_screen()
    print("Sufferance Escape\n")
    print(" ", Fore.RED + "Life" + Fore.RESET + " VS. " + Fore.GREEN + "Human" + Fore.RESET + "\n")
    print("    1 | 2 | 3 ")
    print("   -----------")
    print(f"  1 {format_cell(board[0])} | {format_cell(board[1])} | {format_cell(board[2])} ")
    print("   -----------")
    print(f"  2 {format_cell(board[3])} | {format_cell(board[4])} | {format_cell(board[5])} ")
    print("   -----------")
    print(f"  3 {format_cell(board[6])} | {format_cell(board[7])} | {format_cell(board[8])} ")
    print("\n   " + get_progress_bar(board) + " ")

def format_cell(cell):
    if cell == 'L':
        return Fore.RED + cell
    elif cell == 'H':
        return Fore.GREEN + cell
    else:
        return cell

def check_win(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]            # Diagonals
    ]
    
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return all(cell != ' ' for cell in board)

def get_progress_bar(board):
    num_x = board.count('L')
    num_o = board.count('H')
    empty_bar = '#' * 9

    if num_o + num_x == 0:
        return f"[{empty_bar}]"

    x_bar = Fore.RED + '#' * (9 - num_o)
    o_bar = Fore.GREEN + ('#' * num_o) + Fore.RESET

    return f"[{x_bar}{o_bar}]"

def get_possible_moves(board):
    return [i for i in range(len(board)) if board[i] == ' ']

def minimax(board, player, isMaximizer):
    # Heuristic
    other_player = 'L' if player == 'H' else 'H'
    if check_win(board, player):
        return 1
    if check_win(board, other_player):
        return -1
    if is_board_full(board):
        return 0
    
    # Maximizer
    if isMaximizer:
        value = float("-inf")
        for i in get_possible_moves(board):
            board[i] = player  # Apply move
            value = max(value, minimax(board, other_player, False))  # Maximum value of minimizers
            board[i] = ' '  # Undo move
        return value

    # Minimizer
    value = float("inf")
    for i in get_possible_moves(board):
        board[i] = player  # Apply move
        value = min(value, minimax(board, other_player, True))  # Minimizer value of maximizers
        board[i] = ' '  # Undo move
    return value

def get_best_move(board, player):
    best_value = float("-inf")
    best_move = None

    for i in get_possible_moves(board):
        board[i] = player # Apply move
        value = minimax(board, player, True)
        board[i] = ' ' # Undo move
        
        if value > best_value:
            best_value = value
            best_move = i

    return best_move

def main():
    board = [' '] * 9
    current_player = 'H'
    
    while True:
        print_board(board)
        
        if is_board_full(board):
            print("\nIt's a draw!")
            break
    
        try:
            if current_player == 'H':
                move = input(f"\nPlayer {current_player}, enter your move (row column): ")
                row, col = map(int, move.split())
                index = (row - 1) * 3 + (col - 1)
            else:
                index = get_best_move(board, current_player)

            if board[index] == ' ':
                board[index] = current_player
                if check_win(board, current_player):
                    print_board(board)
                    print(Fore.YELLOW + f"\nPlayer {current_player} wins!")
                    break
                current_player = 'L' if current_player == 'H' else 'H'
            else:
                print("Invalid move. That cell is already taken.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column (e.g., 2 3).")

if __name__ == "__main__":
    main()
