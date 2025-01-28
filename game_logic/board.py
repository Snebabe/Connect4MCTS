from copy import deepcopy

class Board:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
    self.current_player = 1
    self.last_move = None
    self.game_over_cache = None

  def drop_piece(self, col, player):
    for row in reversed(range(self.rows)):
      if self.grid[row][col] == 0:
        self.grid[row][col] = player
        self.last_move = col
        self.current_player = 3 - int(player)
        self.game_over_cache = None
        return
    
    raise ValueError("Column is full")
  
  def is_valid_move(self, col):
    return self.grid[0][col] == 0
  
  def get_untried_moves(self, tried_moves=None):
    valid_moves = self.get_valid_moves()
    if tried_moves is None:
      return valid_moves
    
    return [move for move in valid_moves if move not in tried_moves]
  
  def get_valid_moves(self):
    return [col for col in range(self.cols) if self.is_valid_move(col)]
  
  def is_draw(self):
    return all(self.grid[0][col] != 0 for col in range(self.cols))
  
  def check_win(self, player):
    for row in range(self.rows):
      for col in range(self.cols):
        if self._check_direction(row, col, 1, 0, player) or \
           self._check_direction(row, col, 0, 1, player) or \
           self._check_direction(row, col, 1, 1, player) or \
           self._check_direction(row, col, 1, -1, player):
          return True
  
  def _check_direction(self, row, col, drow, dcol, player):
    count = 0
    for _ in range(4):
      if 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == player:
        count += 1
        if count == 4:
          return True
      
      else:
        break

      row += drow
      col += dcol
    return False
  
  def is_game_over(self):
    if self.game_over_cache is None:
      self.game_over_cache = self.is_draw() or any(self.check_win(player) for player in (1, 2))
    
    return self.game_over_cache
  
  def clone(self):
    new_board = Board(self.rows, self.cols)
    new_board.grid = deepcopy(self.grid)
    new_board.last_move = self.last_move
    new_board.current_player = self.current_player
    return new_board
  
  def __str__(self):
    symbols = {0: "-", 1: "X", 2: "O"}
    display = "\n".join(" ".join(symbols[cell] for cell in row) for row in self.grid)
    return f"\n{display}\n"
