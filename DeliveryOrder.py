

class DeliveryOrder:

    def __init__(self, identifier, route, start_time):
        self.identifier = identifier
        self.route = route
        self.start_time = start_time
        self.current_link_index = 0
        self.number_of_links = len(route.get_links())
        self.completed = False

    def next_link(self):
        self.current_link_index += 1
        if self.current_link_index >= self.number_of_links:
            # this means the drone arrived at target -> delivery order completed
            self.completed = True
            print('Delivery order completed!')
            return None
        return self.route.get_link_at(self.current_link_index)

    def next_link_is_full(self):
        return self.route.get_link_at(self.current_link_index+1).is_full()

    def i_am_on_finish_link(self):
        return (self.route.get_link_at(self.current_link_index) == self.route.links[-1]) and (self.current_link_index == self.number_of_links-1)

    def get_start_link(self):
        if not self.route.links:
            # If the route doesn't exist, return no start link (special case handling for start node equals end node)
            return None
        return self.route.get_link_at(0)

    def is_completed(self):
        return self.completed

    def set_completed(self):
        self.completed = True



