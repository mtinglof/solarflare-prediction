from mainrunner import MainRunner
import copy

class RoundControl(): 
    def __init__(self): 
        #build the main runner and testing object 
        self.runner_obj = MainRunner(100, 100, 1100)
        self.runner_obj.getTestObj()

    def firstRound(self):
        #create starting species and creatures 
        #signal new test round
        #test, sort and set new survival threshold
        creature_collection = self.runner_obj.createStartingCollection()
        self.runner_obj.newTestRound()
        tested_creatures = self.runner_obj.testCreatures(creature_collection)
        new_sorted_creatures = self.runner_obj.sortHerd(tested_creatures)
        while(self.runner_obj.checkSurvival(new_sorted_creatures) == False): 
            print('new sample')
            self.runner_obj.resetTestObj()
            self.runner_obj.newTestRound()
            creature_collection = self.runner_obj.createStartingCollection()
            tested_creatures = self.runner_obj.testCreatures(creature_collection)
            new_sorted_creatures = self.runner_obj.sortHerd(tested_creatures)
        print(len(tested_creatures))
        print(self.runner_obj.min_survival_threshold)
        return(new_sorted_creatures, tested_creatures, self.runner_obj.min_survival_threshold)

    def continueRound(self, new_sorted_creatures, tested_creatures): 
        import copy 
        scores = []
        while(self.runner_obj.checkSurvival(new_sorted_creatures) == True): 
            old_tested_creatures = copy.deepcopy(tested_creatures)
            alive_creatures = self.runner_obj.creatureNaturalSelection(new_sorted_creatures)
            self.runner_obj.newTestRound()
            tested_creatures = self.runner_obj.testCreatures(alive_creatures)
            print(len(tested_creatures))   
            print(self.runner_obj.min_survival_threshold)
            new_sorted_creatures = self.runner_obj.sortHerd(tested_creatures)
            scores.append(self.runner_obj.min_survival_threshold)
        return(old_tested_creatures, scores)

    def newRound(self, old_tested_creatures): 
        self.runner_obj.resetTestObj()
        copy_old_tested_creatures = copy.deepcopy(old_tested_creatures)
        creature_collection = self.runner_obj.speciesNaturalSelection(old_tested_creatures)
        copy_creature_collection = copy.deepcopy(creature_collection)

        self.runner_obj.newTestRound()
        tested_creatures = self.runner_obj.testCreatures(creature_collection)
        new_sorted_creatures = self.runner_obj.sortHerd(tested_creatures)

        while(self.runner_obj.checkSurvival(new_sorted_creatures) == False): 
            print('new sample')
            self.runner_obj.resetTestObj()
            self.runner_obj.newTestRound()
            old_tested_creatures = copy.deepcopy(copy_old_tested_creatures)
            creature_collection = self.runner_obj.speciesNaturalSelection(old_tested_creatures)
            copy_creature_collection = copy.deepcopy(creature_collection)
            tested_creatures = self.runner_obj.testCreatures(creature_collection)
            new_sorted_creatures = self.runner_obj.sortHerd(tested_creatures)

        print(len(tested_creatures))
        print(self.runner_obj.min_survival_threshold)
        return(new_sorted_creatures, tested_creatures, copy_creature_collection, self.runner_obj.min_survival_threshold)