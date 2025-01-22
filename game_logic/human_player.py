from .player import Player
from .board import Board

class HumanPlayer(Player):
  def make_move(self, board: Board):
    while True:
      try:
        col = int(input(f"Enter the col to drop (0-{board.cols - 1}): "))
        if col in board.get_valid_moves():
          return col
        print("Invalid move. Try again")
      
      except ValueError:
        print("Please enter a valid number.")
