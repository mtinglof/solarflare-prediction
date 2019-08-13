import numpy as np 
import random

class Swarm():
    def __init__(self, creature_collection): 
        self.creature_collection = creature_collection
        self.best_position = 0 
        self.interia_coef = 1
        self.acceleration_coef = 1
        self.high = 0
        self.findGlobal()
        self.updateVelocity()
        self.updatedMovement()
        
    def findGlobal(self): 
        sorted_collection = sorted(self.creature_collection, key = lambda timecreaturecreate: timecreaturecreate.getCreature()["last_score"], reverse=True)
        self.best_position = sorted_collection[0].getCreature()['weights']
        self.high = round(sorted_collection[0].getCreature()['last_score'], 4) * 100
        print("high: {}".format(self.high))

    def updateVelocity(self): 
        for creature in self.creature_collection: 
            for index, layer in enumerate(self.best_position): 
                interia = creature.getCreature()['velocity'][index] * self.interia_coef
                best_self_movement = (self.acceleration_coef * random.uniform(0, 1)) * np.subtract(creature.getCreature()['best_position'][index], creature.getCreature()['weights'][index])
                best_social_movement = (self.acceleration_coef * random.uniform(0, 1)) * np.subtract(self.best_position[index], creature.getCreature()['weights'][index])
                velocity = np.add(interia, best_self_movement)
                creature.getCreature()['velocity'][index] = np.add(velocity, best_social_movement)
    
    def updatedMovement(self): 
        for creature in self.creature_collection: 
            for index, layer in enumerate(self.best_position): 
                creature.getCreature()['weights'][index] = np.add(creature.getCreature()['weights'][index], creature.getCreature()['velocity'][index])