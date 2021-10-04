
from xml.etree.ElementTree import ElementTree

import utm
from Link import Link
from Network import Network
from Node import Node


class OpenStreetMapParser:

    def __init__(self, osm_input_file):
        self.osm_input_file = osm_input_file

        # Latitude and longitude to x,y conversion
        self.dx_in_meters = None
        self.dy_in_meters = None

        self.minimum_latitude = None
        self.maximum_latitude = None
        self.minimum_longitude = None
        self.maximum_longitude = None


    def convert_to_network(self):
        tree = ElementTree()
        tree.parse(self.osm_input_file)

        root = tree.getroot()
        # A network consists of nodes and links, so let's create them here
        nodes = []
        links = []

        link_id_counter = 0

        for element in root:
            if element.tag == 'bounds':
                print('bounds detected')
                bounds_element = element
                self.minimum_latitude = float(bounds_element.attrib['minlat'])
                self.maximum_latitude = float(bounds_element.attrib['maxlat'])
                self.minimum_longitude = float(bounds_element.attrib['minlon'])
                self.maximum_longitude = float(bounds_element.attrib['maxlon'])


                self.x_min, self.y_min, *rest = utm.from_latlon(self.minimum_latitude, self.minimum_longitude)
                self.x_max, self.y_max, *rest = utm.from_latlon(self.maximum_latitude, self.maximum_longitude)

                self.dx_in_meters = (self.x_max-self.x_min)
                self.dy_in_meters = (self.y_max-self.y_min)

            elif element.tag == 'node':
                node_element = element
                identifier = int(node_element.get('id'))

                x = self.get_x_from_longitude(float(node_element.get('lon')))
                y = self.get_y_from_latitude(float(node_element.get('lat')))
                z = 0  # OSM is 2D - therefore set z=0
                nodes.append(Node(identifier, x, y, z))


            elif element.tag == 'way':
                way_links = []
                way_element = element

                way_identifier = way_element.get('id')

                nd_elements = [nd_element for nd_element in way_element if nd_element.tag == 'nd']

                for i in range(len(nd_elements) - 1):
                    start_node_identifier = nd_elements[i].get('ref') # The identifiers are stored in the 'ref' attribute of a nd (node) element
                    end_node_identifier = nd_elements[i+1].get('ref')

                    # Get actual nodes by their identifiers so they can be used here to create the link
                    start_node = next(node for node in nodes if node.identifier == int(start_node_identifier))
                    end_node = next(node for node in nodes if node.identifier == int(end_node_identifier))

                    #unique_identifier_string = way_identifier + '-' + start_node_identifier + '-' + end_node_identifier
                    link_identifier = link_id_counter
                    link_id_counter += 1

                    way_links.append(Link(link_identifier, start_node, end_node, capacity=50))

                # Only add discovered way to links, if it is tagged as a highway:
                add_way_links_to_links = False
                for way_subelement in way_element:
                    if way_subelement.tag == 'tag' and way_subelement.get('k') == 'highway':
                        add_way_links_to_links = True

                if add_way_links_to_links:
                    links.extend(way_links)

        # from the above created nodes, only the ones used with links shall be used in the network
        network_nodes = [node for node in nodes if [link for link in links if link.start_node == node or link.end_node == node]]


        return Network(network_nodes, links)



    def get_y_from_latitude(self, latitude: float):
        return self.dy_in_meters * (latitude-self.minimum_latitude)/(self.maximum_latitude-self.minimum_latitude)

    def get_x_from_longitude(self, longitude: float):
        return self.dx_in_meters * (longitude-self.minimum_longitude)/(self.maximum_longitude-self.minimum_longitude)






