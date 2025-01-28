import random
import time
from .node import Node

# only prints if DEBUG = True in config.py
from .utils import dprint_tree, dprint

class MCTS:
  def __init__(self, uct_constant, time_limit=0, limit=0):
      self.time_limit = time_limit
      self.uct_constant = uct_constant
      self.limit = limit
      self.rollouts = 0

  # Ground function to search for a move, includes all steps
  # Select the node with the best UCT score
  # Expand the node 
  def search(self, root_node: Node):
    
    # dprint("Starting search, this is our node:")
    # dprint_tree(root_node)

    end_time = time.time() + self.time_limit
    while time.time() < end_time or self.rollouts < self.limit:
      node = self._select(root_node)
      reward = self._simulate(node)
      self._backpropagate(node, reward)

    return root_node.best_child(uct_constant=0)
  
  def _select(self, node: Node):
    
    dprint("Selecting node from:")
    dprint_tree(node)

    while not node.state.is_game_over():
      if not node.is_fully_expanded():
        return self._expand(node)
        
      node = node.best_child(self.uct_constant)
    return node
  
  def _expand(self, node: Node):
    # Adds a child node playing an untried move
    # from the currrent node's state

    dprint("Expanding on:")
    dprint_tree(node)
    
    untried_moves = node.untried_moves

    for move in untried_moves:
      new_state = node.state.clone()
      new_state.drop_piece(move, node.state.current_player)
      node.add_child(new_state)

    node.untried_moves = []

    return random.choice(node.children)
  
  def _simulate(self, node: Node):
    dprint("Simulating node, this is our node:")
    dprint_tree(node)
    current_state = node.state.clone()
    while not current_state.is_game_over():
      dprint("Playing a random move")
      move = random.choice(current_state.get_valid_moves())
      current_state.drop_piece(move, current_state.current_player)
      dprint("Result state:")
      dprint(current_state)
    
    dprint("Simulation over")
    self.rollouts += 1
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