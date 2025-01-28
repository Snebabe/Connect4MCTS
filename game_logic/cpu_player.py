from .player import Player
from .board import Board
from mcts import MCTS
from mcts import Node
from mcts.utils import print_tree, dprint

class CPUPlayer(Player):
  def __init__(self, id, time_limit=0, simlimit=0):
    super().__init__(id)
    self.time_limit = time_limit
    self.simlimit = simlimit

  def make_move(self, board: Board):
    print("Thinking...")
    root = Node(state=board.clone())
    mcts = MCTS(2**0.5, self.time_limit, self.simlimit)
    best_node = mcts.search(root)
    # print("Best node:")
    # print_tree(best_node, 1)
    # print(best_node.value)
    print(f"Made {mcts.rollouts} rollouts")
    return best_node.state.last_move