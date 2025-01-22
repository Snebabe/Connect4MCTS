def print_tree(node, level=0):
  print(f"{' ' * (2*level)}Node(
        State: {node.state}, 
        Visits: {node.visits}, 
        Value: {node.value})")
  
  for child in node.children:
    print_tree(child, level +1)