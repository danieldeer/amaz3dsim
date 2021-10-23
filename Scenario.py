import logging

import Configuration
from Result import AgentResult, NetworkResult

log = logging.getLogger(__name__)


class Scenario:

    def __init__(self, network, agents):
        self.observers = []

        self.network = network
        self.agents = agents
        self.run_finished = False

    def run(self):
        active_agents = self.agents  # An active agent is every agent who is not finished travelling his route yet
        finished_agents = []
        current_time_step = 0

        while active_agents:  # Run the simulation, as long as there are active agents

            for agent in active_agents:
                if agent.delivery_order.start_time <= current_time_step:  # Start moving an agent once his start_time is reached
                    agent.move()

                if agent.delivery_order.is_completed():  # If a delivery order is completed, then move the active agent to the finished agents
                    active_agents.remove(agent)
                    finished_agents.append(agent)

            if Configuration.loudness_calculation_enabled:
                for link in self.network.links:
                    link.update_loudness()

            for link in self.network.links:
                link.number_of_agents_that_moved_on_this_link_this_timestep = 0

            current_time_step += 1
            self.notify_observers()  # Notifies observers that the simulation has progressed. In this case, the only observer is the Visualizer2D or Visualizer3D (if visualization is active) which will update its image afterward

        log.info('Simulation passed')

        log.info('Creating results...')
        agent_results = []
        for agent in finished_agents:
            result = AgentResult(agent)
            log.info(result.to_string())
            agent_results.append(result)

        network_result = NetworkResult(self.network)

        self.run_finished = True
        self.notify_observers()  # This notify will notify the observers that the simulation is finished. The observer can check the self.run_finished variable to know that it's finished. This is only needed to close the Visualization3D window after the simulation

        return agent_results, network_result

    def add_observer(self, observer):
        self.observers.append(observer)
        log.info('Observer registered: ' + str(observer))

    def notify_observers(self):
        for observer in self.observers:
            observer.notify()
