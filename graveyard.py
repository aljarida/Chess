from pieces import *

class Graveyard:
    def __init__(self, color):
        self.grave = []
        self.color = color
        self.numLost = 0
    
    def __repr__(self):
        repr = self.color.capitalize() + ": " + str(self.grave)
        return repr