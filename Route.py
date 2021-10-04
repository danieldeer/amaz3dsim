

class Route:

    def __init__(self, links):
        self.links = links

    def get_links(self):
        return self.links

    def get_link_at(self, index):
        return self.links[index]

    def get_joined_slot_occupations(self):
        joined_slot_occupations = []
        for link in self.links:
            joined_slot_occupations.extend(link.get_slot_occupations())

    def to_string(self):
        link_ids = []
        for link in self.links:
            link_ids.append('link ' + str(link.identifier))

        return ', '.join(link_ids)




