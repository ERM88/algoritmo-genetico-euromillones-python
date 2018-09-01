import random

class Combination:
    "Represent a euromillions combination"
    #Attribute
    TOTAL_NUMERS = 5
    TOTAL_STARS = 2
    SMALLEST_NUMBER = 1
    BIGGEST_NUMBER = 50
    SMALLEST_STAR = 1
    BIGGEST_STAR = 11
    
    def __init__(self):
        self.numbers = list()   #numbers of the combination
        self.stars = list()     #stars of the combination
        self.value = 0          #value of the combination (average between all comparison with winning combinations) 
        self.values = list()    #list wit all values of the combination (comparison with winning combinations) 
        self.deviation = 0
        
    #Create an euromillions random combination
    def createValidCombination(self):
        self.numbers = self._createChromosome(self.SMALLEST_NUMBER, self.BIGGEST_NUMBER, self.TOTAL_NUMERS)
        self.stars = self._createChromosome(self.SMALLEST_STAR, self.BIGGEST_STAR, self.TOTAL_STARS)
        return self
    #Create a random chromosome: a list with a length equal argument total and all alleles are between smallest and biggest 
    def _createChromosome(self, smallest, biggest, total):
        chromosome = list()
        possible = list(range(smallest, biggest+1))
        
        i = 0
        while i<total:
            position = random.randint(0, len(possible)-1)
            chromosome.append(possible[position])
            del possible[position]
            i+=1
        chromosome.sort(key=None, reverse=False)
        return chromosome
    
    #This combination reproduce with other combination which is passed by parameter
    #Return a list with two sons
    def reproduce(self, other_combination):
        son1 = Combination()
        son2 = Combination()
        numbers = self._reproduceChromosomes(self.numbers, other_combination.numbers, self.SMALLEST_NUMBER, self.BIGGEST_NUMBER, self.TOTAL_NUMERS)
        stars = self._reproduceChromosomes(self.stars, other_combination.stars, self.SMALLEST_STAR, self.BIGGEST_STAR, self.TOTAL_STARS)
        son1.numbers = numbers[0]
        son2.numbers = numbers[1]
        son1.stars = stars[0]
        son2.stars = stars[1]
        sons = [son1, son2]
        return sons
    #Two chomosmes reproduce and the result is return. This is sorted
    def _reproduceChromosomes(self, chromosomes1, chromosomes2, smallest, biggest, total_alleles):
        all_alleles = list()
        chromosome_descendant1 = list()
        chromosome_descendant2 = list()
        
        for allele in chromosomes1:
            all_alleles.append(allele)
        for allele in chromosomes2:
            all_alleles.append(allele)
        all_alleles.sort(key=None, reverse=False)
        
        for i in list(range(smallest, biggest+1)):
            repetitions = all_alleles.count(i)
            if repetitions>1:
                chromosome_descendant1.append(i)
                chromosome_descendant2.append(i)
                all_alleles.remove(i)
                all_alleles.remove(i)
        
        for allele in all_alleles:
            if len(chromosome_descendant1)<total_alleles and len(chromosome_descendant2)<total_alleles:
                son_get_allele = random.random()
                if son_get_allele<0.5:
                    chromosome_descendant1.append(allele)
                else:
                    chromosome_descendant2.append(allele)
            else:
                if len(chromosome_descendant1)==total_alleles:
                    chromosome_descendant2.append(allele)
                else:
                    chromosome_descendant1.append(allele)
        
        chromosome_descendant1.sort(key=None, reverse=False)
        chromosome_descendant2.sort(key=None, reverse=False)
        chromosome_descendants = [chromosome_descendant1, chromosome_descendant2]
        return chromosome_descendants
    
    #Mutate all chromosomes with a maximum ratio of mutation.
    def mutate(self, ratio_max_mutation_numbers, ratio_max_mutation_stars):
        self.numbers = self._mutateChromosome(self. numbers, self.SMALLEST_NUMBER, self.BIGGEST_NUMBER, ratio_max_mutation_numbers)
        self.stars = self._mutateChromosome(self.stars, self.SMALLEST_STAR, self.BIGGEST_STAR, ratio_max_mutation_stars)
        return self
    #Mutate a chromosome with a maximum ratio of mutation.
    #Return the mutated chromosome 
    def _mutateChromosome(self, chromosome, smallest, biggest, ratio_max_mutation):
        possible_alleles = list(range(smallest, biggest+1))
        for allele in chromosome:
            possible_alleles.remove(allele)
        
        i = 0
        for allele in chromosome:
            ratio_mutation = random.random()
            if ratio_mutation<ratio_max_mutation:
                j = random.randint(0, len(possible_alleles)-1)
                allele_aux = chromosome[i]
                chromosome[i] = possible_alleles[j]
                possible_alleles[j] = allele_aux
            i+=1
        chromosome.sort(key=None, reverse=False)
        return chromosome
    
    def rebootValue(self):
        self.value = 0
        self.values = list()
        
    def printInfo(self):
        print("Numbers ")
        for number in self.numbers:
            print("    ", number)
        print("Stars: ")
        for star in self.stars:
            print("    ", star)
        print("Value: ", self.value)
        print("Values: ", self.values)
        