from kenken_csp import *
from propagators import *
from heuristics import *

test_props = True;
test_ord_mrv = True;
test_ord_lcv = True;

boards = [ [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]],
[[4],[11,21,6,3],[12,13,3,0],[14,24,3,1],[22,23,7,0],[31,32,2,2],[33,43,3,1],[34,44,6,3],[41,42,7,0]],
[[5],[11,21,4,1],[12,13,2,2],[14,24,1,1],[15,25,1,1],[22,23,9,0],[31,32,3,1],[33,34,44,6,3],[35,45,9,0],[41,51,7,0],[42,43,3,1],[52,53,6,3],[54,55,4,1]],
[[6],[11,21,11,0],[12,13,2,2],[14,24,20,3],[15,16,26,36,6,3],[22,23,3,1],[25,35,3,2],[31,32,41,42,240,3],[33,34,6,3],[43,53,6,3],[44,54,55,7,0],[45,46,30,3],[51,52,6,3],[56,66,9,0],[61,62,63,8,0],[64,65,2,2]] ]

def print_kenken_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":
    def zigzagLevelOrder(root):
        if not root: return []
        res, temp, stack, flag = [], [], [root], 1
        while stack:
            for i in range(len(stack)):
                node = stack.pop(0)
                temp += [node.val]
                if node.left: stack += [node.left]
                if node.right: stack += [node.right]
            print("temp:",temp[::flag])
            res += [temp[::flag]]
            temp = []
            flag *= -1
        return res


    class Node:
        # Constructor to create a new node
        def __init__(self, data):
            self.val = data
            self.left = self.right = None


    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(7)
    root.left.right = Node(6)
    root.right.left = Node(5)
    root.right.right = Node(4)
    print("Zigzag Order traversal of binary tree is")
    print(zigzagLevelOrder(root))