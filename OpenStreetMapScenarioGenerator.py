import os

import Configuration
from OpenStreetMapParser import OpenStreetMapParser
from ScenarioGenerator import ScenarioGenerator
from ScenarioSerializer import ScenarioSerializer


class OpenStreetMapScenarioGenerator():


    def generate(self, osm_filepath, number_of_agents):
        # Parse the OSM format
        network = OpenStreetMapParser(osm_filepath).convert_to_network()

        # Place agents in the OSM network
        scenario = ScenarioGenerator().generate_scenario_for_given_network(network, number_of_agents)

        return scenario

if __name__ == '__main__':

    # If you want to translate your own osm file into a scenario xml, then execute this .py file (this main method will be called)
    number_of_agents = 500 # Set a number of agents here
    osm_filepath = os.path.join(Configuration.project_filepath, 'test', 'darmstadt-uni.osm') # Set the filepath of the .osm file here

    scenario = OpenStreetMapScenarioGenerator().generate(osm_filepath, number_of_agents)

    relative_scenario_filename = ScenarioSerializer().serialize(scenario, 'osm')
    print('Your .osm file was translated to a scenario.xml file and is located in ' + os.path.join(Configuration.project_filepath, relative_scenario_filename))