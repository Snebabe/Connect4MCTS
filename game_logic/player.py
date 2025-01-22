from abc import ABC, abstractmethod

class Player(ABC):
  def __init__(self, id):
    self.id = id

  @abstractmethod
  def make_move(self, board):
    pass