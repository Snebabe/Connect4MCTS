import random
import time
from .node import Node

class MCTS:
  def __init__(self, time_limit, uct_constant):
      self.time_limit = time_limit
      self.uct_constant = uct_constant

  def search(self, root_node: Node):
    end_time = time.time() + self.time_limit
    while time.time() < end_time:
      node = self._select(root_node)
      reward = self._simulate(node)
      self._backpropagate(node, reward)

    return root_node.best_child(uct_constant=0)
  
  def _select(self, node: Node):
    while not node.state.is_game_over():
      if not node.is_fully_expanded():
        return self._expand(node)
        
      node = node.best_child(self.uct_constant)
    return node
  
  def _expand(self, node: Node):
    untried_moves = node.state.get_untried_moves()
    new_move = random.choice(untried_moves)
    new_state = node.state.clone()
    new_state.drop_piece(new_move, node.state.current_player)
    return node.add_child(new_state)
  
  def _simulate(self, node: Node):
    current_state = node.state.clone()
    while not current_state.is_game_over():
      move = random.choice(current_state.get_valid_moves())
      current_state = current_state.drop_piece(move, current_state.current_player)
    
    if current_state.check_win(1):
      return -1
    if current_state.check_win(2):
      return 1
    if current_state.is_draw():
      return 0
    
  def _backpropagate(self, node: Node, reward):
    while node is not None:
      node.visits += 1
      node.value += reward
      node = node.parent
      reward = -reward