class ContainerSet:
    def __init__(self, *values: Symbol, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value: Symbol):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other: set[Symbol]):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other: set[Symbol]):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other: set[Symbol]):
        return self.update(other) | self.epsilon_update(other)

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return "%s-%s" % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __eq__(self, other):
        return (
            isinstance(other, ContainerSet)
            and self.set == other.set
            and self.contains_epsilon == other.contains_epsilon
        )
        
class DisjointSet:
    def __init__(self, *items):
        self.nodes = { x: DisjointNode(x) for x in items }

    def merge(self, items):
        items = (self.nodes[x] for x in items)
        try:
            head, *others = items
            for other in others:
                head.merge(other)
        except ValueError:
            pass

    @property
    def representatives(self):
        return { n.representative for n in self.nodes.values() }

    @property
    def groups(self):
        return [[n for n in self.nodes.values() if n.representative == r] for r in self.representatives]

    def __len__(self):
        return len(self.representatives)

    def __getitem__(self, item):
        return self.nodes[item]

    def __str__(self):
        return str(self.groups)

    def __repr__(self):
        return str(self)

class DisjointNode:
    def __init__(self, value):
        self.value = value
        self.parent = self

    @property
    def representative(self):
        if self.parent != self:
            self.parent = self.parent.representative
        return self.parent

    def merge(self, other):
        other.representative.parent = self.representative

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)