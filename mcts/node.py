# Node for MCTS
from game_logic.board import Board
from math import sqrt, log, inf

class Node:
  def __init__(self, state: Board, parent=None):
    self.state = state
    self.parent = parent
    self.untried_moves = state.get_untried_moves()
    self.children = []
    self.visits = 0
    self.value = 0.0

  def is_fully_expanded(self):
    # All children expanded?
    return len(self.children) >= len(self.state.get_valid_moves())
  
  def best_child(self, uct_constant = 1.4):
    # Return child with best UCT score
    def uct_score(child: Node):
      # UCT (Upper Confidence Bound)
      # We want to check on moves we believe our good
      # We also want to explore moves we haven't tried yet
      # A high UCT is given to a node that has a high exploitation and low exploration
      # The formula is from wikipedia 
      
      if child.visits == 0:
        return 0 if uct_constant == 0 else inf

      exploitation = child.value / child.visits

      exploration = uct_constant * sqrt(log(self.visits)/child.visits)
      return exploitation + exploration
    
    return max(self.children, key=uct_score)
  
  def add_child(self, child_state):
    # Add child_node for state
    child_node = Node(state=child_state, parent=self)
    self.children.append(child_node)
    return child_node