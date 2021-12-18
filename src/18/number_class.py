class NumberLeaf:
    __slots__ = ["value", "parent", "lex_left", "lex_right"]

    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.lex_left = None
        self.lex_right = None

    def __repr__(self):
        return f"Leaf({self.value})"

    def split(self):
        left = self.value // 2
        right = self.value - left
        new_tree = NumberTree(self.parent, None, None)
        new_tree.left = NumberLeaf(left, new_tree)
        new_tree.right = NumberLeaf(right, new_tree)

        # patch up the tree
        if self.parent.left is self:
            self.parent.left = new_tree
        else:
            assert self.parent.right is self
            self.parent.right = new_tree

        # patch up lexigraphical order
        root = self.parent
        while root.parent is not None:
            root = root.parent
        root.relex()

    @property
    def magnitude(self):
        return self.value


class NumberTree:
    __slots__ = ["left", "right", "parent", "depth"]

    def __init__(self, parent, left, right):
        self.left = left
        self.right = right
        self.parent = parent
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def __repr__(self):
        as_list = self.to_list()
        return f"Tree({repr(as_list)})"

    def __add__(self, other):
        new_tree = NumberTree.from_list([self.to_list(), other.to_list()])
        while new_tree.reduce_iteration():
            pass
        return new_tree

    @classmethod
    def from_list(cls, list_, parent=None):

        left_item, right_item = list_
        new_tree = NumberTree(parent, None, None)

        if isinstance(left_item, list):
            new_tree.left = NumberTree.from_list(left_item, new_tree)
        else:
            new_tree.left = NumberLeaf(left_item, new_tree)

        if isinstance(right_item, list):
            new_tree.right = NumberTree.from_list(right_item, new_tree)
        else:
            new_tree.right = NumberLeaf(right_item, new_tree)

        if new_tree.depth == 0:
            new_tree.relex()
        return new_tree

    @classmethod
    def from_string(cls, line):
        list_ = eval(line)
        return cls.from_list(list_, None)

    def to_list(self):
        if isinstance(self.left, NumberTree):
            left = self.left.to_list()
        else:
            left = self.left.value

        if isinstance(self.right, NumberTree):
            right = self.right.to_list()
        else:
            right = self.right.value
        return [left, right]

    def children(self):
        """Iterate through one level of children"""
        yield self.left
        yield self.right

    def decendents(self):
        """Iterate through all descendents, depth first"""
        for child in self.children():
            if isinstance(child, NumberTree):
                yield from child.decendents()
            yield child

    def decendent_values(self):
        """Iterate through decendents, but only return leaves"""
        for child in self.decendents():
            if isinstance(child, NumberLeaf):
                yield child

    def decendent_trees(self):
        """Iterate through decendents, but only return subtrees"""
        for child in self.decendents():
            if isinstance(child, NumberTree):
                yield child

    def relex(self):
        assert self.depth == 0

        values = self.decendent_values()
        prev = next(values)
        prev.lex_left = None

        for child in values:
            prev.lex_right = child
            child.lex_left = prev
            prev = child

        child.lex_right = None

    def can_explode(self):
        for child in self.decendent_trees():
            if child.depth >= 4:
                return child
        return None

    def explode(self):
        assert isinstance(self.left, NumberLeaf)
        assert isinstance(self.right, NumberLeaf)

        new_leaf = NumberLeaf(0, self.parent)

        if self.left.lex_left:
            self.left.lex_left.value += self.left.value
            self.left.lex_left.lex_right = new_leaf

        if self.right.lex_right:
            self.right.lex_right.value += self.right.value
            self.right.lex_right.lex_left = new_leaf

        new_leaf.lex_left = self.left.lex_left
        new_leaf.lex_right = self.right.lex_right

        if self.parent.left is self:
            self.parent.left = new_leaf
        else:
            assert self.parent.right is self
            self.parent.right = new_leaf

    def can_split(self):
        for child in self.decendent_values():
            if child.value >= 10:
                return child
        return None

    def reduce_iteration(self):
        child = self.can_explode()
        if child:
            child.explode()
            return True

        child = self.can_split()
        if child:
            child.split()
            return True

        return False

    @property
    def magnitude(self):
        return 3 * self.left.magnitude + 2 * self.right.magnitude
