# reference https://github.com/stanislavkozlovski/Red-Black-Tree/blob/master/rb_tree.py

from enum import Enum

class Shades(Enum):
    BLACK = 0
    RED = 1


class RBNode:

    """A red black node.

    Args:
        value (int): the value of the node
        color (Shades.int): the specific color of the node
        parent (RBNode): the parent node
        left (Optional[RBNode]): the left child
        right (Optional[RBNode]): the right child

    """

    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '{color} {val} RBNode'.format(
            color=self.color, value=self.value)

    def __iter__(self):
        """Inorder traversal of the tree"""
        if self.left.value is not None:
            yield from self.left.__iter__()

        yield self.value

        if self.right.value is not None:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.value is None and self.value is other.value:
            return True

        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = (
                self.parent.value == other.parent.value and
                self.parent.color == other.parent.color)
        return (
            self.value == other.value
            and self.color == other.color
            and parents_are_same)

    def has_children(self):
        """
        children are not nils

        Returns:
            bool
        """
        return self.left.value is not None or self.right.value is not None


class RedBlackTree:
    # every node has null nodes as children initially. create one such object
    # for easy management
    NIL_LEAF = RBNode(value=None, color=Shades.BLACK, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None

    def __iter__(self):
        if not self.root:
            return None
        yield from self.root.__iter__()

    def _find_parent(self, value):
        """Finds a place for our value in the binary tree"""
        def inner_find(parent):
            """Find the appropriate parent and the side the next value should be on"""
            if value == parent.value:
                return parent, None
            elif value < parent.value:
                if parent.left.value is None:
                    return parent, 'L'
                return inner_find(parent.left)
            else: # value > parent.value
                if parent.right.value is None:
                    return parent, 'R'
                return inner_find(parent.right)
        return inner_find(self.root)

    def _right_rotation(self, A, X, B, Y, C, to_recolor=None):
        """
        Doing a right rotation


                 Y                            X
               /- -\     right rotate ->    /- -\
             X-     -C   <- left rotate   A-     -Y
           /- -\                                /- -\
         A-     -B                            B-     -C
        """
        X.left = A
        X.right = Y
        Y.left = B
        Y.right = C

        if to_recolor:
            node = to_recolor
            X.color = Shades.BLACK
            node.color = Shades.RED
            Y.color = Shades.RED

    def _left_rotation(self, A, X, B, Y, C, to_recolor=None):
        """
        Doing a right rotation


                 Y                            X
               /- -\     right rotate ->    /- -\
             X-     -C   <- left rotate   A-     -Y
           /- -\                                /- -\
         A-     -B                            B-     -C
        """
        Y.left = X
        Y.right = C
        X.left = A
        X.right = B

        if to_recolor:
            node = to_recolor
            Y.color = Shades.BLACK
            node.color = Shades.RED
            X.color = Shades.RED

    def _recolor(node):
        node.right.color = Shades.BLACK
        node.left.color = Shades.BLACK
        if node != self.root:
            node.color = Shades.RED
        self._try_rebalance(node)

    def _try_rebalance(self, node):
        parent = node.parent
        value = node.value
        if (
            parent is None  # this should not happend
            or parent.parent is None  # parent is the root node
            or (node.color is not Shades.RED or parent.color is not Shades.RED)
        ): # no need to rebalance
            return

        grandfather = parent.parent
        node_direction = 'L' if node.value < parent.value else 'R'
        parent_direction = 'L' if parent == grandfather.left else 'R'
        uncle = grandfather.right if node_direction == 'L' else grandfather.left
        general_direction = parent_direction + node_direction

        # hard case is that the uncle is black
        if uncle == self.NIL_LEAF or uncle.color == Shades.BLACK:
            # rotate
            if general_direction == 'LL':
                self._right_rotation(node, parent.right, parent, grandfather, uncle, to_recolor=node)
            elif general_direction == 'RR':
                self._left_rotation(uncle, grandfather, parent.left, parent, node, to_recolor=node)
            elif general_direction == 'LR':
                raise NotImplementedError("this needs to be completed")
            elif general_direction == 'RL':
                raise NotImplementedError("this needs to be completed")
            else:
                raise ValueError("Not a valid direction: {}".format(general_direction))
        else:
            # easy case is that the uncle is red
            # recolor the nodes
            self._recolor(grandfather)


    def add(self, value):
        # if there is nothing in the tree then we just create the root node
        # with two nill nodes as leafs
        if not self.root:
            self.root = RBNode(
                value=value, color=Shades.BLACK, parent=None,
                left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_direction = self._find_parent(value)

        # if value present in the treee then do nothing
        if node_direction is None:
            return

        new_node = RBNode(
            value=value, color=Shades.RED, parent=parent, left=self.NIL_LEAF,
            right=self.NIL_LEAF)
        if node_direction == 'L':
            parent.left = new_node
        if node_direction == 'R':
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1
        return new_node
