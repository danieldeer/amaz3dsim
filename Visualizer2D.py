from tkinter import *
import math
import random
import time

import numpy as np
from matplotlib import colors

import Configuration
from Link import Link




class PerformanceVisualizer:



    def __init__(self, scenario):
        self.scenario = scenario
        self.SCALE = 1

        width = max([node.x for node in scenario.network.nodes]) * self.SCALE
        height = max([node.y for node in scenario.network.nodes]) * self.SCALE

        self.drawn_agents = []
        self.drawn_links = []

        self.tk = Tk()
        self.tk.title('Visualizer 2D')
        self.canvas = Canvas(self.tk, bg="white", width=width, height=height)
        self.canvas.pack()


        self.colormap = self.create_thesis_colormap()
        self.y_max = height

        self.draw_network()





    def draw_agents(self):
        for canvas_id in self.drawn_agents:
           self.canvas.delete(canvas_id)

        self.drawn_agents = []

        if Configuration.risk_calculation_enabled and self.scenario.agents:
            # The current maximum risk is needed to determine the colors for the agents later
            self.current_max_risk = max(agent.sum_of_risk for agent in self.scenario.agents) + 1

        for agent in self.scenario.agents:
            x,y,z = agent.get_3d_coordinate()

            if Configuration.risk_calculation_enabled:
                colors = self.colormap(np.linspace(0, 1, self.current_max_risk))
                color = colors[agent.sum_of_risk]
                fill_color = color.tolist()
                fill_color = fill_color[:-1]  # Last item is RGB-alpha, which is not needed
                fill_color = self.__from_rgb(tuple([int(color * 255) for color in fill_color]))
            else:
                fill_color = self.__from_rgb((0, 157, 129))

            self.drawn_agents.append(self.__draw_circle_with(x, y, 2, fill_color))

    def __from_rgb(self, rgb):
        #translates an rgb tuple of int to a tkinter friendly color code
        return "#%02x%02x%02x" % rgb

    def draw_network(self):
        if self.drawn_links:
            for canvas_link in self.drawn_links:
                self.canvas.delete(canvas_link)

        self.drawn_links = []

        if Configuration.loudness_calculation_enabled:
            # The current maximum loudness is needed to determine the colors for the links later
            self.current_max_loudness = max(link.sum_of_loudness for link in self.scenario.network.links) + 1


        for link in self.scenario.network.links:
            self.drawn_links.append(self.__draw_link(link))  # loop over all streets in the street network and draw each one

        if Configuration.visualization_show_nodes:
            for node in self.scenario.network.nodes:
                self.__draw_circle_with(node.x, node.y, 1, 'darkgrey')

    def __draw_link(self, link: Link):


        if Configuration.loudness_calculation_enabled:
            colors = self.colormap(np.linspace(0, 1, self.current_max_loudness))
            color = colors[link.sum_of_loudness]
            fill_color = color.tolist()
            fill_color = fill_color[:-1] # Last item is RGB-alpha, which is not needed
            fill_color = self.__from_rgb(tuple([int(color*255) for color in fill_color]))
        else:
            fill_color = 'darkgrey'


        return self.canvas.create_line(link.start_node.x*self.SCALE, self.y_max - link.start_node.y*self.SCALE,
                           link.end_node.x * self.SCALE, self.y_max - link.end_node.y*self.SCALE,
                           width=1*self.SCALE,
                           fill=fill_color)

    def __draw_circle_with(self, center_point_x, center_point_y, radius, fill):
        # Ovals (or circles) in tkinter are drawn from one corner to the other
        # however, we want to draw a circle with a center point and a radius
        # so we have to determine the corner coordinates first
        upper_left_corner_x = (center_point_x - radius)* self.SCALE
        upper_left_corner_y = self.y_max - (center_point_y - radius)* self.SCALE

        lower_right_corner_x = (center_point_x + radius)* self.SCALE
        lower_right_corner_y = self.y_max - (center_point_y + radius)* self.SCALE

        # draw and return the circle specified by its corners with the given (fill) color and no outline
        return self.canvas.create_oval(upper_left_corner_x, upper_left_corner_y, lower_right_corner_x, lower_right_corner_y, fill=fill
                                  )

        # The animations shall be in colors suiting to the thesis
    def create_thesis_colormap(self):
        # This dictionary defines the colormap
        cdict = {'red': ((0, 0.0, 0.0),  # no red at 0
                         (1.0, 192 / 255, 192 / 255)),  # set to 0.8 so its not too bright at 1

                 'green': ((0.0, 157 / 255, 157 / 255),  # set to 0.8 so its not too bright at 0
                           (1.0, 0.0, 0.0)),  # no green at 1

                 'blue': ((0.0, 129 / 255, 129 / 255),  # no blue at 0
                          (1.0, 0.0, 0.0))  # no blue at 1
                 }

        # Create the colormap using the dictionary
        return colors.LinearSegmentedColormap('GnRd', cdict)



    def notify(self):
        if Configuration.loudness_calculation_enabled:
            self.draw_network()

        self.draw_agents()
        self.canvas.update()
        self.canvas.after(int(Configuration.visualization_frame_time * 1000))





