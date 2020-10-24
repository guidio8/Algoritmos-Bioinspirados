# coding: utf-8
import math
import numpy as np
import random
import sys
import os
import pandas as pd

tam_pop = int(sys.argv[3] )
geracoes = int(sys.argv[4])
chance_mutacao = float(sys.argv[1])
taxa_cruzamento = float(sys.argv[2])
execucao = sys.argv[5]
instancia = sys.argv[6]
dimensao = 2
populacao = []
alpha = 0.75
beta = 0.25

#print("EU RECEBI O ARGUMETNO DO TXT: ", tam_pop)

def func_obj(x):
	n = float(len(x))
	f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))

	t = 0
	for i in range(0, len(x)):
		t += np.cos(2 * math.pi * x[i])

	s_exp = 1/n * t
	f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
    
	return f

class Individuo:
	def __init__(self, dimensao):
		self.real = []
		#Quando cada individuo possuir mais do que uma dimensão, cada um vai ser uma matriz onde cada coluna é uma representação binária
		for i in range(dimensao):
			self.real.append(GerarIndividuo())
		self.fitness = 0
#funcao que gera uma representação binária aleatória de 6 dígitos para cada indivíduo
def GerarIndividuo():
	return random.uniform(-2,2)

def Roleta(populacao):
	pais_vencedores = []
	roleta = []
	fit_aux = []
	total = 0
	qtd_pais = 0

	for i in populacao:
		if i.fitness > 0:
			fit_aux.append(1/i.fitness)
		elif i.fitness == 0:
			fit_aux.append(1)
		total += fit_aux[-1]		
	for i in range(len(fit_aux)):
		roleta.append(fit_aux[i]/total)
	
	while qtd_pais < tam_pop:
		r = random.random()
		soma = 0
		aux = -1
		for i in roleta:
			if(soma < r):
				soma = soma + i
				aux+=1
		pais_vencedores.append(aux)
		qtd_pais+=1

	return pais_vencedores

def CruzamentoAlphaBeta(pai1, pai2, populacao, pop_aux):
	d = []
	X = populacao[pai1]
	Y = populacao[pai2]
	Xfilho = Individuo(dimensao)
	Yfilho = Individuo(dimensao)
	chance_cruzamento = random.random()
	if(chance_cruzamento <= taxa_cruzamento):
		for i in range(dimensao):

			d.append(abs(X.real[i] - Y.real[i]))
			if(X.real[i] <= Y.real[i]):
				u = random.uniform(X.real[i] - alpha * d[i], Y.real[i] + beta * d[i])
				Xfilho.real[i] = u
				u = random.uniform(X.real[i] - alpha * d[i], Y.real[i] + beta * d[i])
				Yfilho.real[i] = u
			else:
				u = random.uniform(Y.real[i] - beta * d[i], X.real[i] + alpha * d[i])
				Xfilho.real[i] = u
				u = random.uniform(X.real[i] - beta * d[i], X.real[i] + alpha * d[i])
				Yfilho.real[i] = u
			pop_aux.append(Xfilho)
			pop_aux.append(Yfilho)
	else:
		pop_aux.append(X)
		pop_aux.append(Y)

def Elitismo(populacao):
	fitness = 1000
	indice = 0
	for i in range(len(populacao)):
		if populacao[i].fitness < fitness:
			fitness = populacao[i].fitness
			indice = i
	
	return indice

def Mutacao(individuo):
	indice = random.randrange(0, dimensao -1)
	individuo.real[indice] = random.random()

def EscreveArquivo(media, desvio, melhor_fitness, instancia, execucao):
	folder_name = 'tabelas'
	if not os.path.exists(folder_name):
	    os.makedirs(folder_name)
	    os.chdir(folder_name)
	else:
	    os.chdir(folder_name)
	path = ""
	file_name = 'file' + instancia + '.csv'
	f = open(file_name, "+a")
	f.write(execucao + ',' + str(media) + ',' + str(desvio) + ',' + str(melhor_fitness) + '\n')

vetor_fitness = []

#gera uma população com individuos aleatórios
for i in range(tam_pop):
	populacao.append(Individuo(dimensao))
#calcula o fitness de cada indivíduo
for i in populacao:
	i.fitness = func_obj(i.real)
#começa o AG
atual = 1
while atual < geracoes:
	indice_ganhadores = Roleta(populacao)
	#print("ganhadores\n", indice_ganhadores)
	pop_aux = []
	n_cruz = 0
	while n_cruz < len(indice_ganhadores):
		CruzamentoAlphaBeta(indice_ganhadores[n_cruz],indice_ganhadores[n_cruz+1], populacao, pop_aux)
		n_cruz+=2
	for i in pop_aux:
		c_mut = random.random()
		if c_mut <= chance_mutacao:
			Mutacao(i)
	elitismo = Elitismo(populacao)
	#A função de elitismo serve para saber o índice do indivíduo com melhor (no caso, menor) fitness
	armazenar = populacao[elitismo]
	#gera um individuo auxiliar e temporário para ser armazenado na população "final" da geração, que vai substituir alguém aleatóriamente
	#garantindo que o melhor individuo sempre esteja nas populações futuras
	populacao = pop_aux[:]
	indi_aleatorio = random.randrange(0, len(populacao))
	populacao[indi_aleatorio] = armazenar

	for i in populacao:
		i.fitness = func_obj(i.real)
		#print(i.fitness)
	atual += 1

for i in populacao:
	vetor_fitness.append(i.fitness)

melhor_fitness = min(vetor_fitness)
media = np.mean(vetor_fitness)
desvio = np.std(vetor_fitness)

EscreveArquivo(media, desvio, melhor_fitness, instancia, execucao)
