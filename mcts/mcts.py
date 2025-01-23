import random
import time
from .node import Node
from .utils import print_tree, dprint

class MCTS:
  def __init__(self, time_limit, uct_constant):
      self.time_limit = time_limit
      self.uct_constant = uct_constant

  # Ground function to search for a move, includes all steps
  # Select the node with the best UCT score
  # Expand the node 
  def search(self, root_node: Node):
    dprint("Starting search, this is our node:")
    print_tree(root_node)
    end_time = time.time() + self.time_limit
    while time.time() < end_time:
      node = self._select(root_node)
      reward = self._simulate(node)
      self._backpropagate(node, reward)

    return root_node.best_child(uct_constant=0)
  
  def _select(self, node: Node):
    dprint("Selecting node from:")
    print_tree(node)
    while not node.state.is_game_over():
      if not node.is_fully_expanded():
        return self._expand(node)
        
      node = node.best_child(self.uct_constant)
    dprint("Returning this node:")
    print_tree(node)
    return node
  
  def _expand(self, node: Node):
    # Get untried moves
    # Choose a move and remove it from the untried moves
    # Create a new state that plays the move
    # The new state gets added as a child node
    
    # From the child node a simulation will be run
    # Not here
    dprint("Expanding on:")
    print_tree(node)
    untried_moves = node.untried_moves

    new_move = random.choice(untried_moves)
    node.untried_moves.remove(new_move)

    new_state = node.state.clone()
    new_state.drop_piece(new_move, node.state.current_player)

    dprint("Expanded with this child:")
    dprint(new_state)
    return node.add_child(new_state)
  
  def _simulate(self, node: Node):
    dprint("Simulating node, this is our node:")
    print_tree(node)
    current_state = node.state.clone()
    while not current_state.is_game_over():
      dprint("Playing a random move")
      move = random.choice(current_state.get_valid_moves())
      current_state.drop_piece(move, current_state.current_player)
      dprint("Result state:")
      dprint(current_state)
    
    dprint("Simulation over")
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