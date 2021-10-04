import logging
import os
import time

from Visualizer2D import PerformanceVisualizer
from ScenarioParser import ScenarioParser
from Visualizer3D import Visualizer
import Configuration
from ResultsSerializer import ResultsSerializer
from ScenarioGenerator import ScenarioGenerator

logging.basicConfig(level=os.environ.get('LOGLEVEL', Configuration.log_level))
log = logging.getLogger(__name__)


def main():
    start = time.time()

    simulate()

    end = time.time()
    elapsed_millis = round((end - start) * 1000)
    log.info('Time spent in simulate() is: ' + str(elapsed_millis) + 'ms')


def simulate():
    log.info('Multi-Agent Graph Simulator started')

    if Configuration.random_mode:
        # Generate random scenario
        scenario = ScenarioGenerator().generate(Configuration.random_scenario_number_of_nodes, Configuration.random_scenario_number_of_agents)
    else:
        # Parse scenario from input file
        parser = ScenarioParser(Configuration.input_file)
        scenario = parser.get_scenario()

    if Configuration.visualization_active:
        if Configuration.visualization_3D_active:
            network_plotter = Visualizer(scenario)
        else:
            network_plotter = PerformanceVisualizer(scenario)

        scenario.add_observer(network_plotter)

    agent_results, network_result = scenario.run()

    serializer = ResultsSerializer(agent_results, network_result)
    serializer.write()


if __name__ == '__main__':
    log.error('Please call CommandLineInterface.py from the command line')
