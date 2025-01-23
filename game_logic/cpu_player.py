from .player import Player
from .board import Board
from mcts import MCTS
from mcts import Node

class CPUPlayer(Player):
  def __init__(self, id, time_limit):
    super().__init__(id)
    self.time_limit = time_limit

  def make_move(self, board: Board):
    print("Thinking...")
    root = Node(state=board.clone())
    mcts = MCTS(self.time_limit, 2**0.5)
    best_node = mcts.search(root)
    return best_node.state.last_move