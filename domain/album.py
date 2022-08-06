
class Album():

    def __init__(self, year, name):
        self.year = year
        self.name = name
        self.decade = year - (year % 10)

    def __gt__(self, other:'Album'):
        if self.year == other.year:
            return self.name > other.name
        else:
            return self.year > other.year
    
    def __lt__(self, other:'Album'):
        if self.year == other.year:
            return self.name < other.name
        else:
            return self.year < other.year

    
    def __repr__(self):
        return "{0} {1}".format(self.year, self.name)