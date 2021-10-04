
class Battery:

    def __init__(self, battery_life, agent):
        self.battery_life = battery_life
        self.agent = agent

    def discharge(self):
        raise NotImplementedError('Has to be implemented by the subclass')