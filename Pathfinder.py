import logging

import networkx as nx
from networkx import NetworkXNoPath

from Route import Route

log = logging.getLogger(__name__)

class Pathfinder:

    def __init__(self):
        self.G = None

    # Finds the shortest route in the network between the given start and end node.
    # Returns None if no route is found.
    def get_shortest_route(self, network, start_node, end_node):

        if self.G is None:
            self.G = self.get_graph_from_network(network)

        try:
            shortest_path = nx.astar_path(self.G, start_node, end_node)
            log.info('Path discovered between node ' + str(start_node.identifier) + ' and ' + str(end_node.identifier))
        except NetworkXNoPath:
            log.debug('No path found between node ' + str(start_node.identifier) + ' and ' + str(end_node.identifier))
            return None

        links = []
        for i in range(0, len(shortest_path)-1):
            start_node = shortest_path[i]
            end_node = shortest_path[i+1]
            edge_data = self.G.get_edge_data(start_node, end_node, default='Edge not found')
            links.append(edge_data['link'])

        return Route(links)

    def get_graph_from_network(self, network):
        self.G = nx.DiGraph()

        for link in network.links:
            self.G.add_edge(link.start_node, link.end_node, weight=link.length, link=link)

        return self.G
