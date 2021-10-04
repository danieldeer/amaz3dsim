from math import sqrt

import Configuration
from Battery import Battery


class BatteryHeightDifferenceBased(Battery):

    def __init__(self, battery_life, agent):
        super().__init__(battery_life, agent)
        self.current_z = self.get_current_agent_height()
        self.current_x, self.current_y = self.get_current_agent_horizontal_position()

    def discharge(self):
        self.old_z = self.current_z
        self.current_z = self.get_current_agent_height()
        vertical_distance = self.current_z - self.old_z

        # Discharge for vertical movement (height difference)
        if vertical_distance > 0:
            self.battery_life -= int(vertical_distance * Configuration.battery_model_vertical_discharge_factor)

        # Discharge for horizontal movement
        self.old_x, self.old_y = self.current_x, self.current_y
        self.current_x, self.current_y = self.get_current_agent_horizontal_position()
        horizontal_distance = sqrt((self.current_x-self.old_x)**2 + (self.current_y - self.old_y)**2)

        self.battery_life -= int(abs(horizontal_distance) * Configuration.battery_model_horizontal_discharge_factor)


    def get_current_agent_height(self):
        x, y, z = self.agent.get_3d_coordinate()
        return int(z)

    def get_current_agent_horizontal_position(self):
        x, y, z = self.agent.get_3d_coordinate()
        return int(x), int(y)


