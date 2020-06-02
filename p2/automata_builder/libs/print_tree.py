from ..tree.node import Node

COUNT =[10]

def print2DUtil(root, space) : 
    # Base case  
    if (root == None) : 
        return
  
    # Increase distance between levels  
    space += COUNT[0] 
  
    # Process right child first  
    if isinstance(root.right, Node):
        print2DUtil(root.right, space)  
  
    # Print current node after space  
    # count  
    print()  
    for _ in range(COUNT[0], space): 
        print(end = " ")
    yeet = root.operation
    if root.operation == ' ':
        yeet = '&'

    if isinstance(root.right, Node):
        if isinstance(root.left, Node):
            print(str(root.left.id) + str(yeet) + str(root.right.id))
        else:
            print(str(root.left) + str(yeet) + str(root.right.id))
    elif isinstance(root.left, Node):
        print(str(root.left.id) + str(yeet) + str(root.right))
    else:
        print(str(root.left) + str(yeet) + str(root.right))
  
    # Process left child  
    if isinstance(root.left, Node):
        print2DUtil(root.left, space)
  
# Wrapper over print2DUtil()  
def print2D(root) : 
      
    # space=[0] 
    # Pass initial space count as 0  
    print2DUtil(root, 0)