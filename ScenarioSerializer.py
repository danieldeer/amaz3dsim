# Given a scenario object, this class is responsible for generating the scenario.xml file
from pathlib import Path
from xml.dom import minidom
from xml.dom.minidom import Element
from xml.etree.ElementTree import Element, SubElement, tostring

import Configuration

class ScenarioSerializer:

    def serialize(self, scenario, target_directory):
        scenario_element = Element('scenario')

        network_element = SubElement(scenario_element, 'network')
        nodes_element = SubElement(network_element, 'nodes')
        for node in scenario.network.nodes:
            node_element = SubElement(nodes_element, 'node',
                                       {
                                           'id': str(node.identifier),
                                           'x': str(node.x),
                                           'y': str(node.y),
                                           'z': str(node.z)
                                       })
        links_element = SubElement(network_element, 'links')
        for link in scenario.network.links:
            link_element = SubElement(links_element, 'link',
                                       {
                                           'id': str(link.identifier),
                                           'from': str(link.start_node.identifier),
                                           'to': str(link.end_node.identifier),
                                           'capacity': str(link.capacity)
                                       })

        agents_element = SubElement(scenario_element, 'agents')
        for agent in scenario.agents:
            agent_element = SubElement(agents_element, 'agent',
                                       {
                                           'id': str(agent.identifier),
                                           'speed': str(agent.speed),
                                           'deliveryOrderId': str(agent.delivery_order.identifier)
                                       })

        delivery_orders_element = SubElement(scenario_element, 'deliveryOrders')
        for agent in scenario.agents:
            delivery_order = agent.delivery_order
            start_node_id = delivery_order.route.links[0].start_node.identifier
            end_node_id = delivery_order.route.links[-1].end_node.identifier
            delivery_order_element = SubElement(delivery_orders_element, 'deliveryOrder',
                                       {
                                           'id': str(delivery_order.identifier),
                                           'startNodeId': str(start_node_id),
                                           'endNodeId': str(end_node_id),
                                           'startTime': str(delivery_order.start_time)
                                       })

            # Create route only if a route is present in the delivery order
            if delivery_order.route:
                route_element = SubElement(delivery_order_element, 'route')
                for link in delivery_order.route.links:
                    link_id_element = SubElement(route_element, 'linkId')
                    link_id_element.text = str(link.identifier)

        filename = self.__generate_filename(scenario, target_directory)
        self.__write(scenario_element, filename)
        return filename

    def __write(self, scenario_element, filename):
        if Configuration.prettify_output:
            xml = self.__prettify(scenario_element)
        else:
            xml = tostring(scenario_element).decode('utf-8')

        # Create target directory if it does not exist
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        with open(filename, 'w') as f:
            f.write(xml)

    # Returns a prettier version of the xml output to improve readability
    def __prettify(self, element):
        # source: https://pymotw.com/2/xml/etree/ElementTree/create.html
        rough_string = tostring(element, 'utf-8')
        pretty_xml = minidom.parseString(rough_string).toprettyxml(indent='  ')
        return pretty_xml

    def __generate_filename(self, scenario, target_directory):
        return target_directory + '/' + str(len(scenario.network.nodes)) + 'nodes' + str(len(scenario.agents)) + 'agents-scenario.xml'
