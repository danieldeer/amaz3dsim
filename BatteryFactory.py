import Configuration
import Constants
from BatterySimple import BatterySimple
from BatteryHeightDifferenceBased import BatteryHeightDifferenceBased

# The BatteryFactory is responsible for returning the correct battery object depending on the configuration
def get_battery(battery_life, agent):
    battery_model = Configuration.battery_model

    if battery_model == Constants.battery_model_simple:
        return BatterySimple(battery_life, agent)

    if battery_model == Constants.battery_model_height_difference:
        return BatteryHeightDifferenceBased(battery_life, agent)
