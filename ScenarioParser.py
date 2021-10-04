import logging
from xml.etree.ElementTree import ElementTree

import lxml.etree

from Link import Link
from Network import Network
from Node import Node
from Pathfinder import Pathfinder
import Configuration
from Agent import Agent
from DeliveryOrder import DeliveryOrder
from Route import Route
from Scenario import Scenario

log = logging.getLogger(__name__)


class ScenarioParser:

    def __init__(self, path_to_xml):
        self.path_to_schema = Configuration.schema_file
        tree = ElementTree()
        tree.parse(path_to_xml)

        root = tree.getroot()

        if Configuration.schema_validation_active:
            self.__validate_network_xml(path_to_xml)

        self.__convert_to_scenario(root)
        self.pathfinder = None

    def __validate_network_xml(self, path_to_xml):
        xml_file = lxml.etree.parse(
            path_to_xml)  # https://www.kite.com/python/answers/how-to-validate-an-xml-file-with-an-xml-schema-in-python
        xml_validator = lxml.etree.XMLSchema(file=self.path_to_schema)
        is_valid = xml_validator.validate(xml_file)
        if not is_valid:
            raise Exception('Input scenario XML does not validate against scenario XSD')
        else:
            log.info('Input validated against XSD')

    def __convert_to_scenario(self, root):
        self.__convert_to_network(root)
        self.__convert_to_delivery_orders(root)
        self.__convert_to_agents(root)

        # To generate the full scenario, passing delivery_orders explicitly is not needed, since delivey_orders are
        # already held by the agents
        self.scenario = Scenario(self.network, self.agents)

    def __convert_to_network(self, root):
        # A network consists of nodes and links, so let's create them here
        nodes = []
        links = []

        network_element = root.find('network')

        nodes_element = network_element.find('nodes')
        for node_element in nodes_element:
            identifier = int(node_element.get('id'))
            x = int(node_element.get('x'))
            y = int(node_element.get('y'))
            z = int(node_element.get('z'))
            nodes.append(Node(identifier, x, y, z))

        links_element = network_element.find('links')
        for link_element in links_element:
            identifier = int(link_element.get('id'))
            start_node_identifier = int(link_element.get('from'))
            end_node_identifier = int(link_element.get('to'))
            capacity = int(link_element.get('capacity'))

            # Find correct start and end_node by ID
            start_node = next((node for node in nodes if node.identifier == start_node_identifier),
                              None)  # source: https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi
            end_node = next((node for node in nodes if node.identifier == end_node_identifier), None)
            links.append(Link(identifier, start_node, end_node, capacity))

        self.network = Network(nodes, links)

    # The method below must be called after __convert_to_delivery_order, so that the self.delivery_orders list is filled
    # Otherwise we can't find the delivery_order by id
    def __convert_to_agents(self, root):
        # To instantiate agents, we need speed and delivery order id
        agents = []

        agents_element = root.find('agents')
        for agent_element in agents_element:
            identifier = int(agent_element.get('id'))
            speed = int(agent_element.get('speed'))
            delivery_order_id = int(agent_element.get('deliveryOrderId'))
            delivery_order = next((delivery_order for delivery_order in self.delivery_orders if
                                   delivery_order.identifier == delivery_order_id), None)

            # Optional arguments
            battery_life = None
            if 'batteryLife' in agent_element.attrib:
                battery_life = int(agent_element.get('batteryLife'))

            agents.append(Agent(identifier, speed, delivery_order, battery_life=battery_life))

        self.agents = agents

    def __convert_to_delivery_orders(self, root):
        delivery_orders = []

        delivery_orders_element = root.find('deliveryOrders')
        for delivery_order_element in delivery_orders_element:
            identifier = int(delivery_order_element.get('id'))
            start_node_identifier = int(delivery_order_element.get('startNodeId'))
            end_node_identifier = int(delivery_order_element.get('endNodeId'))
            start_time = int(delivery_order_element.get('startTime'))

            # Find correct start and end_node by ID
            start_node = next((node for node in self.network.nodes if node.identifier == start_node_identifier),
                              None)  # source: https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi
            end_node = next((node for node in self.network.nodes if node.identifier == end_node_identifier), None)

            # To create the route, we have to get the links of the route, if a route was specified
            # OR else calculate the shortest route using A* pathfinder algorithm
            route_element = delivery_order_element.find('route')
            links = []
            if route_element is not None:
                for link_id_element in route_element:
                    link = next((link for link in self.network.links if link.identifier == int(link_id_element.text)), None)
                    links.append(link)
                route = Route(links)
            else:
                log.info('No route specified for delivery order ' + str(identifier) + '. Attempting to calculate '
                                                                                      'shortest route using A* '
                                                                                      'pathfinding algorithm...')

                route = Pathfinder().get_shortest_route(self.network, start_node, end_node)
                if route is not None:
                    log.info('Shortest route is: ' + route.to_string())
                else:
                    log.error('Route does not exist, simulator has to shut down. Please ensure that a route exists between the nodes. All links are unidirectional.')
                    exit()

            delivery_orders.append(DeliveryOrder(identifier, route, start_time))

        self.delivery_orders = delivery_orders

    def get_scenario(self):
        return self.scenario
