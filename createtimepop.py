from timecreaturecreate import TimeCreatureCreate

def CreatePop(size): 
    creature_collection = []
    for x in range(0, size): 
        creature = TimeCreatureCreate()
        creature.createWeights()
        creature_collection.append(creature)
    return(creature_collection)