import logging

log = logging.getLogger(__name__)

# The results class represents the result of the simulation
class AgentResult:

    def __init__(self, agent):
        self.agent = agent

    def get_total_distance(self):
        return sum(link.length for link in self.agent.delivery_order.route.links)

    def get_total_movement_time(self):
        return self.agent.movement_time

    def get_remaining_battery(self):
        return self.agent.battery.battery_life

    def get_sum_of_risk(self):
        return self.agent.sum_of_risk

    def get_max_risk(self):
        return self.agent.max_risk

    def to_string(self):
        return 'Agent ' + str(self.agent.identifier) + ':\t' + str(self.get_total_movement_time()) + ' time units moved\t' + str(self.get_total_distance()) + ' distance units moved'


class NetworkResult:

    def __init__(self, network):
        self.network = network
