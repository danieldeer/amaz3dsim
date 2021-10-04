

class Node:

    def __init__(self, identifier, x, y, z):
        self.identifier = identifier
        # A node in 3D space
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

        self.incoming_links = []
        self.outgoing_links = []

    def add_incoming_link(self, link):
        self.incoming_links.append(link)

    def add_outgoing_link(self, link):
        self.outgoing_links.append(link)

    def equals(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z
