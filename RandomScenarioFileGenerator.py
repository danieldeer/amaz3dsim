from ScenarioSerializer import ScenarioSerializer
from ScenarioGenerator import ScenarioGenerator


class RandomScenarioFileGenerator:

    # The target directory is the directory
    def generate_file(self, number_of_nodes, number_of_agents, target_directory):

        scenario = ScenarioGenerator().generate(number_of_nodes, number_of_agents)

        ScenarioSerializer().serialize(scenario, target_directory)


if __name__ == '__main__':
    RandomScenarioFileGenerator().generateFile(5,5)