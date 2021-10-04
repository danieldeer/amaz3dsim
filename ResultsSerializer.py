import sys
import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring

import Configuration


# The results serializer converts the results into XML
class ResultsSerializer:

    def __init__(self, agent_results, network_result):
        self.agent_results = agent_results
        self.network_result = network_result

    def convert_agent_result_to_xml_elements(self, result):
        top = Element('agent_result', {
            'agent_id': str(result.agent.identifier)
        })

        child = SubElement(top, 'movement_time')
        child.text = str(result.get_total_movement_time())

        child = SubElement(top, 'distance')
        child.text = str(result.get_total_distance())

        child = SubElement(top, 'battery')
        child.text = str(result.get_remaining_battery())

        if Configuration.risk_calculation_enabled:
            risk_element = SubElement(top, 'risk')

            child = SubElement(risk_element, 'sum_of_risk')
            child.text = str(result.get_sum_of_risk())

            child = SubElement(risk_element, 'max_risk')
            child.text = str(result.get_max_risk())

        return top

    def convert_network_result_to_xml_elements(self):
        top = Element('network_result')

        for link in self.network_result.network.links:
            link_element = SubElement(top, 'link', {
                'link_id': str(link.identifier)
            })

            child = SubElement(link_element, 'sum_of_loudness')
            child.text = str(link.sum_of_loudness)

            child = SubElement(link_element, 'max_loudness')
            child.text = str(link.max_loudness)

        return top

    def write(self):
        top = Element('results')
        comment = Comment('RGBSim output')
        top.append(comment)
        for agent_result in self.agent_results:
            top.append(self.convert_agent_result_to_xml_elements(agent_result))

        if Configuration.loudness_calculation_enabled:
            # The network result is only relevant for loudness results
            top.append(self.convert_network_result_to_xml_elements())

        if (Configuration.prettify_output):
            xml = self.prettify(top)
        else:
            xml = tostring(top).decode('utf-8')

        with open(Configuration.output_file, 'w') as f:
            f.write(xml)

    # Returns a prettier version of the xml output to improve readability
    def prettify(self, element):
        # source: https://pymotw.com/2/xml/etree/ElementTree/create.html
        rough_string = tostring(element, 'utf-8')
        pretty_xml = minidom.parseString(rough_string).toprettyxml(indent='  ')
        return pretty_xml
