import logging
import os

import matplotlib
import numpy as np
from matplotlib import pyplot as plt, colors

import Configuration

logging.basicConfig(level=os.environ.get('LOGLEVEL', Configuration.log_level))
log = logging.getLogger(__name__)


class Visualizer:

    def __init__(self, scenario):
        self.scenario = scenario
        self.network = scenario.network
        self.current_points = []
        self.current_agent_points = []
        self.current_agent_with_risk_points = []
        self.current_network_3d_links = []
        self.plotted_links = []

        plt.ion()
        self.fig = plt.figure(figsize=(16,16), dpi=80)
        self.ax = self.fig.add_subplot(111, projection='3d')
        #self.ax.view_init(azim=0, elev=90) # Set top view (x-y plane, birds perspective) as default

        if Configuration.visualization_axis_enabled:
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_zlabel('z')
        else:
            self.ax.set_axis_off()

        self.plot_network()

    def plot_network(self):
        if Configuration.visualization_show_nodes:
            self.plot_nodes()

        self.plot_links()

    def plot_nodes(self):
        if self.current_points:
            self.current_points.remove()

        for node in self.network.nodes:
            self.current_points = self.ax.scatter(node.x, node.y, node.z, facecolor='black')

    def plot_links(self):
        if self.plotted_links:
            for plotted_link in self.plotted_links:
                line = plotted_link[0]
                line.remove()
                del line

        self.plotted_links = []

        colormap = self.create_thesis_colormap()

        if Configuration.loudness_calculation_enabled:
            current_max_loudness = max(link.sum_of_loudness for link in self.network.links) + 1

        for link in self.network.links:
            if Configuration.loudness_calculation_enabled:
                colors = colormap(np.linspace(0, 1, current_max_loudness))
                color = colors[link.sum_of_loudness]
            else:
                color = 'grey'

            self.plotted_links.append(self.ax.plot([link.start_node.x, link.end_node.x],
                                                   [link.start_node.y, link.end_node.y],
                                                   [link.start_node.z, link.end_node.z],
                                                   color=color))

    def plot(self):
        if self.current_agent_points:
            for point in self.current_agent_points:
                point.remove()

        self.current_agent_points = []


        if Configuration.risk_calculation_enabled and self.scenario.agents:
            current_max_risk = max(agent.current_risk for agent in self.scenario.agents) + 1

        current_agent_risks = []
        for agent in self.scenario.agents:

            x_agent, y_agent, z_agent = agent.get_3d_coordinate()

            if Configuration.risk_calculation_enabled:
                colormap = self.create_thesis_colormap()
                colors = colormap(np.linspace(0, 1, current_max_risk))
                color = colors[agent.current_risk]
            else:
                color = Configuration.color_rmr_green

            self.current_agent_points.append(self.ax.scatter(x_agent, y_agent, z_agent, s=100, color=color, alpha=1, edgecolor=Configuration.color_black))

        plt.show()
        plt.pause(Configuration.visualization_frame_time)


    # The animations shall be in colors suiting to the thesis
    def create_thesis_colormap(self):
        # This dictionary defines the colormap
        cdict = {'red': ((0, 0.0, 0.0),  # no red at 0
                         (1.0, 192/255, 192/255)),  # set to 0.8 so its not too bright at 1

                 'green': ((0.0, 157/255, 157/255),  # set to 0.8 so its not too bright at 0
                           (1.0, 0.0, 0.0)),  # no green at 1

                 'blue': ((0.0, 129/255, 129/255),  # no blue at 0
                          (1.0, 0.0, 0.0))  # no blue at 1
                 }

        # Create the colormap using the dictionary
        return colors.LinearSegmentedColormap('GnRd', cdict)




    def notify(self):
        log.debug('Visualizer notification received -> have to update the plot')
        if self.scenario.run_finished:
            plt.close(self.fig)
        else:
            if Configuration.loudness_calculation_enabled:
                self.plot_links()
            self.plot()


