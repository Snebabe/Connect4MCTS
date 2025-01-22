# Node for MCTS
from game_logic.board import Board

class Node:
  def __init__(self, state: Board, parent=None):
    self.state = state
    self.parent = parent
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
      # TODO: Add more info
      exploitation = child.value / (child.visits)
      exploration = uct_constant * (self.visits/child.visits)**0.5
      return exploitation + exploration
    
    return max(self.children, key=uct_score)
  
  def add_child(self, child_state):
    # Add child_node for state
    child_node = Node(state=child_state, parent=self)
    self.children.append(child_node)
    return child_node