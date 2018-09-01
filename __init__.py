import random
import sqlite3
import urllib
import math
from xml.dom.minidom import parse, parseString

from urllib.request import urlopen
from Combination import Combination
from Tournament import Tournament

__author__ = "Enrique Rodriguez Moron"

total_winning_combination = 10

def readFile(nombre):
    infile = open(nombre, 'r')
    lines = list()
    for line in infile:
        lines.append(line)
    infile.close()
    return lines

def fileToCombination(file):
    winning_combinations = list()
    
    for line in file:
        line = line.replace("\t", " ")
        line = line.replace("\n", "")
        if (len(line)!=0) and (len(winning_combinations)<total_winning_combination):
            list_numbers_stars = line.split(" ")
            i = 0
            combination = Combination()
            for number_star in list_numbers_stars:
                if len(number_star)>0:
                    if i<5:
                        combination.numbers.append(int(number_star))
                    else:
                        combination.stars.append(int(number_star))
                    i+=1
            winning_combinations.append(combination)
    return winning_combinations




def probabilidad():
    fichero = readFile("premios2012.txt")
    combinaciones_ganadoras = fileToCombination(fichero)
    print(len(combinaciones_ganadoras))
    repeticiones_numeros = dict.fromkeys(list(range(1, 51)), 0)
    repeticiones_estrellas = dict.fromkeys(list(range(1, 12)), 0)
    for combinacion in combinaciones_ganadoras:
        for numero in combinacion.numeros:
            repeticiones_numeros[numero] += 1
        for estrella in combinacion.estrellas:
            repeticiones_estrellas[estrella] += 1
    numeros = list()
    cantidad_numeros_necesarios = 5
    while(len(numeros)<cantidad_numeros_necesarios):
        max = -1
        numero = list()
        for i in repeticiones_numeros:
            if repeticiones_numeros[i]>max:
                numero = list()
                numero.append(i)
                max = repeticiones_numeros[i]
            elif repeticiones_numeros[i]==max:
                numero.append(i)
        for i in numero:
            numero_repeticion = list()
            numero_repeticion.append(i)
            numero_repeticion.append(max)
            numeros.append(numero_repeticion)
            repeticiones_numeros.pop(i)
            
        
    estrellas = list()
    cantidad_estrellas_necesarios = 2 
    while(len(estrellas)<cantidad_estrellas_necesarios):
        max = -1
        estrella = list()
        for i in repeticiones_estrellas:
            if repeticiones_estrellas[i]>max:
                estrella = list()
                estrella.append(i)
                max = repeticiones_estrellas[i]
            elif repeticiones_estrellas[i]==max:
                estrella.append(i)
        for i in estrella:
            estrella_repeticion = list()
            estrella_repeticion.append(i)
            estrella_repeticion.append(max)
            estrellas.append(estrella_repeticion)
            repeticiones_estrellas.pop(i)
    print(numeros)
    print(estrellas)

def createFirstGeneration(total_fathers):
    fathers = list()
    i = 0
    while i<total_fathers:
        combination = Combination()
        combination = combination.createValidCombination()
        fathers.append(combination)
        i+=1
    return fathers

def reproduceCombinations(combinations):
    combinations.sort(key=lambda combination: combination.value, reverse=False)
        
    sons = list()
    #Se borran los cuatro peores para que pasen automaticamente el mejor, el segundo y los hijos de estos
    i = 0
    while i<4:
        del combinations[0]
        i+=1
    #Se asegura que se crucen el mejor y el segundo mejor
    best_combinations_sons = combinations[len(combinations)-1].reproduce(combinations[len(combinations)-2])
    sons.append(combinations[len(combinations)-1])
    sons.append(combinations[len(combinations)-2])
    sons.append(best_combinations_sons[0])
    sons.append(best_combinations_sons[1])
    #Se hacen los cruces de manera aleatoria
    while len(combinations)>0:
        #Se eligen a los padres
        position_father = random.randint(0, len(combinations)-1)
        father1 = combinations[position_father]
        del combinations[position_father]
        position_father = random.randint(0, len(combinations)-1)
        father2 = combinations[position_father]
        del combinations[position_father]
        #Se reproducen
        current_sons = father1.reproduce(father2)
        sons.append(current_sons[0])
        sons.append(current_sons[1])
        del current_sons[1]
        del current_sons[0]
        del current_sons
    #Devuelve los descendientes        
    return sons

def mutateCombinations(combinations, ratio_max_mutation_numbers, ratio_max_mutation_stars):
    combinations.sort(key=lambda combination: combination.value, reverse=False)
    i = 0
    for combination in combinations:
        if i!=(len(combinations)-1):
            combination = combination.mutate(ratio_max_mutation_numbers, ratio_max_mutation_stars)
            combinations[i] = combination
        i+=1
    return combinations

def geneticAlgorithm():
    ratio_initial_max_mutation_numbers = 0.4
    ratio_initial_max_mutation_stars = 0.5
    ratio_max_mutation_numbers = ratio_initial_max_mutation_numbers
    ratio_max_mutation_stars = ratio_initial_max_mutation_stars
    total_fathers = 500
    total_generations = 100
    tournament_size = 5
    
    file = readFile("premios2012.txt")
    winning_combinations = fileToCombination(file)
    fathers = createFirstGeneration(total_fathers)
    
    count_generations = 0
    tournament = Tournament()
    
    while count_generations<total_generations:
        print("Generacion: " , count_generations)
        if count_generations%10==0:
            tournament_size+=1
            ratio_max_mutation_numbers -= 0.015
            ratio_max_mutation_stars -= 0.019
        count_generations+=1
        
        fathers = tournament.valueAll(fathers, winning_combinations)
        fathers = tournament.fightTournament(fathers, winning_combinations, total_fathers, tournament_size)
        sons = reproduceCombinations(fathers)
        sons = tournament.valueAll(sons, winning_combinations)
        sons = mutateCombinations(sons, ratio_max_mutation_numbers, ratio_max_mutation_stars)
        sons = tournament.valueAll(sons, winning_combinations)
        
        sons.sort(key=lambda combination: combination.value, reverse=False)
        fathers = sons
        
        best_combination = sons[len(sons)-1]
        best_combination.printInfo()

geneticAlgorithm()