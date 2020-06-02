from .node import Node

# testnode = Node(1,2,0)
# testnode.add_operation('|')
# tnode2 = Node(testnode, None, 1)
# tnode2.add_operation('*')

# testnode.p_node()
# tnode2.p_node()

#class to find the deepest node in a binary tree
class FindDeepestNode:

    #max_level keeps track of maximum level
    #res keeps the value of the deepest node so far.
    #level keeps the level of the root
    def find(self, root, level, max_level, res):

        if root !=None:
            level+=1
            if isinstance(root.left, Node):
                self.find(root.left, level, max_level, res)

            #update level and res
            if level > max_level[0]:

                res[0] = root
                max_level[0] = level
            if isinstance(root.right, Node):
                self.find(root.right, level, max_level, res)

    #function for finding the deepest node.
    def deepest_node(self,root):

        #initialization
        res = [-1]
        max_level = [-1]

        self.find(root, 0, max_level, res)
        return res[0]

