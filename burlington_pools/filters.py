

class DropUninterestingEvents:
    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):

        reject_names = [
            'Healing Waters',
            ' 55+',
            "Men's only",
            "Water Running",
            "Aquafit",  # TODO: Reconsider
            # "Lap Swim",
        ]
        for n in reject_names:
            if n in item['name']:
                return False

        if 'Leisure Swim' == item['name'] and 'Tansley Woods Community Centre' == item['location']:
            return False  # only wading pool is open?

        if 'Leisure Pool' == item['facility']:
            return False  # only wading pool is open?

        return True
    
