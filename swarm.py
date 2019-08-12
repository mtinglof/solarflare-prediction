class swarm():
    def __init__(creature_collection, self): 
        self.creature_collection = creature_collection
        self.best_position = 0 
        
    def findGlobal(self): 
        sorted_collection = sorted(self.creature_collection, key = lambda i: i["last_score"], reverse=True)
        self.best_position = sorted_collection[0].getCreature()['weights']
