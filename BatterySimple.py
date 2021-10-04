
from Battery import Battery


class BatterySimple(Battery):

    def __init__(self, battery_life, agent):
        super().__init__(battery_life, agent)

    def discharge(self):
        self.battery_life -= 1

