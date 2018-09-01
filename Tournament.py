import random
import math
from Combination import Combination

class Tournament:
    
    #Current combinations will fight to reproduce in the next generation. Only the strongest will pass
    #They will fight in tournaments which will have a specific size
    #The frist thing is to value all combinations which want to reproduce
    def fightTournament(self, combinations, winning_combinations, total_fathers, tournament_size):
        #combinations = self.valueAll(combinations, winning_combinations)
        
        winning_fathers = list()
        combinations.sort(key=lambda combination: combination.value, reverse=False)
        winning_fathers.append(combinations[len(combinations)-1])
        
        while len(winning_fathers)<total_fathers:
            combinations_will_fight = list()
            i = 0
            while i<tournament_size:
                position = random.randint(0, len(combinations)-1)
                combinations_will_fight.append(combinations[position])
                i+=1
            combinations_will_fight.sort(key=lambda combination: combination.value, reverse=True)
            winning_fathers.append(combinations_will_fight[0])
        return winning_fathers
    
    def valueAll(self, combinations, winning_combinations):
        i = 0
        for combination in combinations:
            combinations[i] = self._valueOne(combination, winning_combinations)
            i+=1
        return combinations
    
    def _valueOne(self, combination, winning_combinations):
        combination.value = 0
        combination.values = list()
        combination.deviation = 0
        
        for winning_combination in winning_combinations:
            total_equal_numbers = 0
            total_equal_stars = 0
            value = 0
            
            for combination_number in combination.numbers:
                for winning_combination_number in winning_combination.numbers:
                    if combination_number==winning_combination_number:
                        total_equal_numbers+=1
                        
            for combination_star in combination.stars:
                for winning_ccombination_star in winning_combination.stars:
                    if combination_star==winning_ccombination_star:
                        total_equal_stars+=1
            
            if total_equal_numbers==5:
                if total_equal_stars==2:
                    value = 20
                elif total_equal_stars==1:
                    value = 16
                else:
                    value = 15
            elif total_equal_numbers==4:
                if total_equal_stars==2:
                    value = 14
                elif total_equal_stars==1:
                    value = 13
                else:
                    value = 12
            elif total_equal_numbers==3:
                if total_equal_stars==2:
                    value = 11
                elif total_equal_stars==1:
                    value = 9
                else:
                    value = 8
            elif total_equal_numbers==2:
                if total_equal_stars==2:
                    value = 10
                elif total_equal_stars==1:
                    value = 6
                else:
                    value = 5
            elif total_equal_numbers==1:
                if total_equal_stars==2:
                    value = 7
                elif total_equal_stars==1:
                    value = 4
                else:
                    value = 2
            else:
                if total_equal_stars==2:
                    value = 3
                elif total_equal_stars==1:
                    value = 1
                else:
                    value = 0
            combination.value += value
            combination.values.append(value)
        combination.value/=len(winning_combinations)
        for value_in_combination in combination.values:
            combination.deviation += pow(value_in_combination, 2)
        combination.deviation/=len(winning_combinations)
        combination.deviation-= pow(combination.value, 2)
        combination.deviation = math.sqrt(combination.deviation)
        combination.value -= combination.deviation
        
#        for value_in_combination in combination.values:
#            combination.deviation += abs(value_in_combination-combination.value)
#        combination.deviation/=len(winning_combinations)
#        combination.value -= combination.deviation
        return combination

