# Run game
from game_logic.board import Board
from game_logic.human_player import HumanPlayer
from game_logic.cpu_player import CPUPlayer
from config import BOARD_ROWS, BOARD_COLS

def main():
  print("Connect-4!")

  board = Board(BOARD_ROWS, BOARD_COLS)

  player1 = HumanPlayer(1)
  # player2 = HumanPlayer(2)
  player2 = CPUPlayer(2, 10, 10000)


  current_player = player1

  while not board.is_game_over():
    print(board)
    print(f"Player {current_player.id}'s turn")

    move = current_player.make_move(board)
    board.drop_piece(move, current_player.id)

    if board.check_win(current_player.id):
      print(board)
      print(f"Player {current_player.id} wins!")
      return
    
    if board.is_draw():
      print(board)
      print("It's a draw!")

    current_player = player1 if current_player == player2 else player2

if __name__ == "__main__":
  main()