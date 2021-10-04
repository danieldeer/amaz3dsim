import logging
import os
import pathlib
import sys

import yaml

# Constant part of configuration (not changeable)

project_filepath = str(pathlib.Path(__file__).parent.resolve())
default_configuration_file = os.path.join(project_filepath, 'config', 'config.yaml')
is_initialized = False



color_rmr_green = (0,157/255,129/255)
color_black = (0, 0, 0)
color_dark_red =(192/255,0,0)


config_filepath = None

input_file = None
output_file = None
schema_file = None
schema_validation_active = None
prettify_output = None

log_level = None

visualization_active = False
visualization_frame_time = 0.1
visualization_axis_enabled = False
visualization_show_nodes = False

slot_resolution = 1

battery_model = None

battery_model_vertical_discharge_factor = None
battery_model_horizontal_discharge_factor = None

random_mode = None

risk_checking_radius = None

risk_calculation_enabled = None
loudness_calculation_enabled = None

random_scenario_node_connection_radius = 10000 # Default
random_scenario_diameter = None
random_scenario_agent_minimum_speed = None
random_scenario_agent_maximum_speed = None
random_scenario_link_capacity = None

def initialize_configuration(input_file, output_file, config_file, random_mode):
    this = sys.modules[__name__]

    this.input_file = input_file
    this.output_file = output_file

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    this.schema_file = os.path.join(project_filepath, cfg['schema_file'])
    this.schema_validation_active = cfg['schema_validation_active']
    this.prettify_output = cfg['prettify_output']

    this.log_level = cfg['log_level']

    this.visualization_active = cfg['visualization_active']
    this.visualization_frame_time = cfg['visualization_frame_time']
    this.visualization_axis_enabled = cfg['visualization_axis_enabled']
    this.visualization_show_nodes = cfg['visualization_show_nodes']
    this.visualization_3D_active = cfg['visualization_3D_active']


    this.slot_resolution = cfg['slot_resolution']

    this.battery_model = cfg['battery_model']

    this.battery_model_vertical_discharge_factor = cfg['vertical_discharge_factor']
    this.battery_model_horizontal_discharge_factor = cfg['horizontal_discharge_factor']

    this.random_mode = random_mode

    this.risk_checking_radius = cfg['risk_checking_radius']

    this.risk_calculation_enabled = cfg['risk_calculation_enabled']
    this.loudness_calculation_enabled = cfg['loudness_calculation_enabled']

    this.random_scenario_node_connection_radius = cfg['random_scenario_node_connection_radius']
    this.random_scenario_diameter = cfg['random_scenario_diameter']
    this.random_scenario_number_of_nodes = cfg['random_scenario_number_of_nodes']
    this.random_scenario_number_of_agents = cfg['random_scenario_number_of_agents']
    this.random_scenario_agent_minimum_speed = cfg['random_scenario_agent_minimum_speed']
    this.random_scenario_agent_maximum_speed = cfg['random_scenario_agent_maximum_speed']
    this.random_scenario_link_capacity = cfg['random_scenario_link_capacity']

    this.is_initialized = True