

class Network:

    def __init__(self, nodes, links):
        self.nodes = nodes
        self.links = links

    def get_link_by_id(self, identifier):
        # Find correct start and end_node by ID
        result = next((link for link in self.links if link.identifier == identifier))
        return result
