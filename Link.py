import numpy

import Configuration


class Link:

    def __init__(self, identifier, start_node, end_node, capacity):
        self.identifier = identifier

        self.start_node = start_node
        self.start_node.add_outgoing_link(self)

        self.end_node = end_node
        self.end_node.add_incoming_link(self)

        self.capacity = capacity

        self.length = int(numpy.sqrt((start_node.x-end_node.x)**2
                                 + (start_node.y-end_node.y)**2
                                 + (start_node.z-end_node.z)**2))

        if self.length == 0: # This applies to very short links from OpenStreetMap data
            self.length = 1

        self.number_of_slots = int(Configuration.slot_resolution * self.length)


        self.slot_occupations = [False] * self.number_of_slots

        self.current_loudness = 0
        self.max_loudness = 0
        self.sum_of_loudness = 0

        # Never can more agents move than the capacity allows
        # Therefore this number has to be tracked
        self.number_of_agents_that_moved_on_this_link_this_timestep = 0

    def update_loudness(self):
        # Loudness is proportional to the number of agents on this link - therefore we measure it this way
        self.current_loudness = sum(self.slot_occupations)

        if self.current_loudness > self.max_loudness:
            self.max_loudness = self.current_loudness

        self.sum_of_loudness += self.current_loudness

    def get_number_of_slots(self):
        return self.number_of_slots

    def is_full(self):
        return sum(self.slot_occupations) >= self.capacity

    def get_slot_occupations(self):
        return self.slot_occupations

    def set_slot_occupation_at(self, index):
        self.slot_occupations[index] = True

    def unset_slot_occupation_at(self, index):
        self.slot_occupations[index] = False


