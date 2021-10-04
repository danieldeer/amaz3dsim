import random

import networkx as nx
import numpy as np

import Configuration
from Node import Node
from Link import Link
from Network import Network
from DeliveryOrder import DeliveryOrder
from Pathfinder import Pathfinder
from Agent import Agent
from Scenario import Scenario


if not Configuration.is_initialized:
    Configuration.initialize_configuration(None, None, Configuration.default_configuration_file, None)


class ScenarioGenerator:

    def __init__(self):
        self.network = None
        self.delivery_orders = None
        self.agents = None
        self.AGENT_SPEED_RANGE = [Configuration.random_scenario_agent_minimum_speed, Configuration.random_scenario_agent_maximum_speed]

    def generate(self, number_of_nodes, number_of_agents):

        radius = Configuration.random_scenario_node_connection_radius # All nodes within this radius will be connected - this is set so high to generate a fully connected graph
        # Generate a network
        self.__generate_network(number_of_nodes, radius)
        # Generate delivery orders
        number_of_delivery_orders = number_of_agents
        self.__generate_delivery_orders(number_of_delivery_orders)
        # Generate agents
        self.__generate_agents(number_of_agents)

        return Scenario(self.network, self.agents)


    # This method shall be used when a network is already provided (eg. generate full scenario from network generated
    # from OpenStreetMap data
    def generate_scenario_for_given_network(self, network: Network, number_of_agents: int):
        # Network is already present
        self.network = network
        # Generate delivery orders
        number_of_delivery_orders = number_of_agents
        self.__generate_delivery_orders(number_of_delivery_orders)
        # Generate agents
        self.__generate_agents(number_of_agents)
        return Scenario(self.network, self.agents)

    def __generate_network(self, n_nodes, radius):
        # Source: https://www.idtools.com.au/3d-network-graphs-python-mplot3d-toolkit/
        # Generate a dict of positions
        scenario_diameter = Configuration.random_scenario_diameter
        pos = {i: (random.uniform(0, scenario_diameter), random.uniform(0, scenario_diameter), random.uniform(0, scenario_diameter)) for i in
               range(n_nodes)}

        # Create random 3D network
        G = nx.random_geometric_graph(n_nodes, radius, pos=pos)

        nodes = []
        links = []
        node_id_counter = 0
        link_id_counter = 0
        for i, j in enumerate(G.edges()):
            x = np.array((pos[j[0]][0], pos[j[1]][0]))
            y = np.array((pos[j[0]][1], pos[j[1]][1]))
            z = np.array((pos[j[0]][2], pos[j[1]][2]))

            startNode = Node(node_id_counter, x[0], y[0], z[0])
            node_id_counter += 1
            endNode = Node(node_id_counter, x[1], y[1], z[1])
            node_id_counter += 1

            # Only add the node to the nodes list if the nodes list does not already contain a matching node (to prevent duplicates)
            if not any(startNode.equals(otherNode) for otherNode in nodes):
                nodes.append(startNode)
            else:
                # A matching node is found in the list - use this matching node
                startNode = next(otherNode for otherNode in nodes if startNode.equals(otherNode))

            if not any(endNode.equals(otherNode) for otherNode in nodes):
                nodes.append(endNode)
            else:
                # A matching node is found in the list - use this matching node
                endNode = next(otherNode for otherNode in nodes if endNode.equals(otherNode))

            capacity = Configuration.random_scenario_link_capacity
            links.append(Link(link_id_counter, startNode, endNode, capacity))
            link_id_counter += 1

        self.network = Network(nodes, links)

    def __generate_delivery_orders(self, number_of_delivery_orders):
        self.delivery_orders = [self.__generate_delivery_order(i) for i in range(number_of_delivery_orders)]

    def __generate_delivery_order(self, delivery_order_id):
        # Generate delivery order

        # Select random start and endnode and check if a route exists
        route = None
        while route is None:
            start_node = random.choice(self.network.nodes)
            end_node = random.choice(self.network.nodes)

            if start_node.identifier is not end_node.identifier:
                route = Pathfinder().get_shortest_route(self.network, start_node, end_node)

        start_time = random.randrange(20)  # Generate random start_time from 0 to 20 seconds

        return DeliveryOrder(delivery_order_id, route, start_time)

    def __generate_agents(self, number_of_agents):
        # Generate agents
        self.agents = [self.__generate_agent(i) for i in range(number_of_agents)]

    def __generate_agent(self, identifier):
        speed = random.choice(range(self.AGENT_SPEED_RANGE[0], self.AGENT_SPEED_RANGE[1]))
        # Assign delivery orders by id -> agent 1 gets delivery order 1, agent 2 delivery order 2, ...
        delivery_order = next(
            delivery_order for delivery_order in self.delivery_orders if delivery_order.identifier == identifier)
        return Agent(identifier, speed, delivery_order, None)


if __name__ == '__main__':
    ScenarioGenerator().generate(20, 20)
