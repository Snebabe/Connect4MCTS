from .node import Node
from config import DEBUG

def dprint(msg):
  if DEBUG: print(msg)

def print_tree(node: Node, level=0):
  if not DEBUG: return
  
  print(f"{' ' * (2*level)}Node(State: {node.state}Visits: {node.visits}, Value: {node.value})")
  
  for child in node.children:
    print_tree(child, level +1)