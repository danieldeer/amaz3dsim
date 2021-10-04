import logging

import Configuration
import BatteryFactory

log = logging.getLogger(__name__)


class Agent:

    DEFAULT_BATTERY_LIFE = 3600

    def __init__(self, identifier, speed, delivery_order, battery_life):
        self.identifier = identifier
        self.speed = int(speed * Configuration.slot_resolution) # Agent speed is given in distance units per second - but internally we have to use slots per second
        self.delivery_order = delivery_order
        self.current_link = delivery_order.get_start_link()
        self.previous_position = None
        self.position = 0
        self.current_link.set_slot_occupation_at(self.position)
        self.movement_time = 0

        self.current_risk = 0
        self.sum_of_risk = 0
        self.max_risk = 0

        if battery_life is None:
            battery_life = Agent.DEFAULT_BATTERY_LIFE

        self.battery = BatteryFactory.get_battery(battery_life, self)

    # We assume that move() is called every simulation step (which is 1 second in real life) starting from the start
    # of the delivery_order
    def move(self):
        if self.current_link is None:
            log.warning('Link is None')
            return
        if self.delivery_order.is_completed():
            log.warning('Agent ' + str(self.identifier) + ' completed delivery order -> does not move.')
            return

        self.movement_time += 1

        if Configuration.risk_calculation_enabled:
            self.__calculate_risk()

        self.__move_on_link()

        self.battery.discharge()



    def __move_on_link(self):
        if self.is_space_before_me_occupied():
            # if someone is too close to me, I can't move
            log.debug(str(self.identifier) + ': Space before me occupied, cannot move')
            return

        if (self.position + self.speed) < self.current_link.get_number_of_slots():
            # I am free to move within a link
            self.__move_position_according_to_speed()
            log.debug(str(self.identifier) + ': Much space, moved freely')
        else:
            # I am nearing the end of the link and have to switch to the next link

            if self.delivery_order.i_am_on_finish_link():
                # I am finished!
                self.current_link.unset_slot_occupation_at(self.position)
                self.position = self.current_link.get_number_of_slots() - 1
                # do not set a new slot occupation
                self.delivery_order.set_completed()

            elif self.delivery_order.next_link_is_full():
                # But the next link is full (capacity limit), therefore I can't move
                log.debug(str(self.identifier) + ': Next link full, cannot move')
            else:
                # I can switch to the next link and start there from position zero
                self.current_link.unset_slot_occupation_at(self.position)
                self.current_link = self.delivery_order.next_link()
                self.position = 0
                self.current_link.set_slot_occupation_at(self.position)
                log.debug(str(self.identifier) + ': Switched link')

    def __move_position_according_to_speed(self):
        self.current_link.unset_slot_occupation_at(self.position)
        self.position += self.speed
        self.current_link.set_slot_occupation_at(self.position)

    def is_space_before_me_occupied(self):
        # Returns if from the current position, another agent is visible within the range of speed or up to the end of the link
        if (self.position + self.speed) < self.current_link.get_number_of_slots():
            return True in self.current_link.slot_occupations[self.position + 1:(self.position + self.speed)]
        else:
            return True in self.current_link.slot_occupations[
                           self.position + 1:]  # the construct in brackets [] returns all elements starting from position, until end of list https://stackoverflow.com/questions/621354/how-to-slice-a-list-from-an-element-n-to-the-end-in-python

    def __calculate_risk(self):
        radius = int(Configuration.risk_checking_radius)

        number_of_agents_within_radius = 0

        # Scan the previous and next links for agents if the radius overlaps to the previous or next links
        if self.position - radius < 0:
            length_to_be_scanned_on_previous_links = abs(self.position - radius)

            # Get the previous links
            if self.current_link.start_node.incoming_links:
                for link in self.current_link.start_node.incoming_links:
                    number_of_agents_within_radius += sum(link.slot_occupations[-length_to_be_scanned_on_previous_links:])

            # Get the previous links
            if self.current_link.start_node.outgoing_links:
                for link in self.current_link.start_node.outgoing_links:
                    if link is not self.current_link:
                        number_of_agents_within_radius += sum(
                            link.slot_occupations[-length_to_be_scanned_on_previous_links:])

        if self.position + radius >= self.current_link.length:
            length_to_be_scanned_on_next_links = abs(self.position + radius - self.current_link.length)

            # Get the next links
            if self.current_link.end_node.outgoing_links:
                for link in self.current_link.end_node.outgoing_links:
                    number_of_agents_within_radius += sum(link.slot_occupations[:length_to_be_scanned_on_next_links])

            # Also consider the links that are incoming in the end node
            if self.current_link.end_node.incoming_links:
                for link in self.current_link.end_node.incoming_links:
                    if link is not self.current_link:
                        number_of_agents_within_radius += sum(link.slot_occupations[-length_to_be_scanned_on_next_links:])

        # Finally, also check the agents on the current link
        if self.position - radius >= 0 and self.position + radius < self.current_link.length: # This means the radius is fully contained on the current link
            number_of_agents_within_radius += sum(self.current_link.slot_occupations[self.position-radius:self.position+radius]) - 1

        elif self.position - radius >= 0 and self.position + radius >= self.current_link.length: # This means that the radius overlaps the end node of the current link
            number_of_agents_within_radius += sum(self.current_link.slot_occupations[self.position - radius:]) -1

        elif self.position - radius < 0 and self.position + radius <= self.current_link.length: # This means that the radius overlaps the start node of the current link
            number_of_agents_within_radius += sum(self.current_link.slot_occupations[:self.position+radius]) - 1
        else:
            # This is the case when the radius overlaps both start and end node of the current link (radius covers the full link)
            number_of_agents_within_radius += sum(self.current_link.slot_occupations) - 1


        # In case an agent is new, and it has not moved yet, and it is on an empty link, the link will have no slot occupations. Risk can be set to 0 in this case
        if self.current_link.slot_occupations[self.position] == False:
            number_of_agents_within_radius = 0

        self.current_risk = number_of_agents_within_radius
        self.sum_of_risk += self.current_risk

        if self.current_risk > self.max_risk:
            self.max_risk = self.current_risk

        log.debug('Agent ' + str(self.identifier) + ' risk ' + str(self.current_risk))

    def get_progress(self):
        return self.position / self.current_link.get_number_of_slots()

    def get_3d_coordinate(self):
        x = self.current_link.start_node.x + self.get_progress() * (
                    self.current_link.end_node.x - self.current_link.start_node.x)
        y = self.current_link.start_node.y + self.get_progress() * (
                    self.current_link.end_node.y - self.current_link.start_node.y)
        z = self.current_link.start_node.z + self.get_progress() * (
                    self.current_link.end_node.z - self.current_link.start_node.z)

        return x, y, z

