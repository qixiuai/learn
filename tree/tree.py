
class Node(object):

    def __init_(self, id, parent_id, children_ids):
        self._id = id
        self._name = name
        self._parent_id = parent_id
        self._children_ids = children_ids
        
    @property
    def id(self):
        return self._id;

    @property
    def name(self):
        return self._name
    
    @property
    def parent(self):
        return self._parent_id

    @property
    def children(self):
        return self._children_ids


class Tree(object):

    def __init__(self, nodes):
        # nodes is a list of node
        # sort nodes to enable binary search
        self._sorted_nodes = sorted(nodes, key=lambda node: node.id)

    def search(self, node_id):
        # TODO binary search
        idx = self._sorted_nodes.index(node_id)
        children = self.sorted_nodes[idx].children
        children_ids = list(map(lambda child: child.id), children)
        return children_ids
        
    
    


