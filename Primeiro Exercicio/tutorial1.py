# coding: utf-8
import math
import numpy as np
import random

dimensao = 2
populacao = []
tam_pop = 100
atual = 1
geracoes = 5
media = 0.0

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
		self.binario = []
		#Quando cada individuo possuir mais do que uma dimensão, cada um vai ser uma matriz onde cada coluna é uma representação binária
		for i in range(dimensao):
			self.binario.append(GerarIndividuo())
		self.fitness = 0
#funcao que gera uma representação binária aleatória de 6 dígitos para cada indivíduo
def GerarIndividuo():
	individuo = []
	for i in range(6):
		x = random.random()
		if x > 0.5:
			individuo.append(1)
		else:
			individuo.append(0)
	return individuo

def RepresentacaoReal(individuo):
	xmin = -2
	xmax = 2
	n = 6
	vetor_de_reais = []
	for i in individuo.binario:
		xReal = xmin + ((xmax - xmin)/(2**n -1)) * intBin(i, n)
		vetor_de_reais.append(xReal)

	return vetor_de_reais

def intBin(bin, n):
	valor = 0 
	for i in range(0, n):
		valor += 2**i * bin[i]
	return valor

def Torneio(populacao):
	pais_vencedores = [] #indice no vetor populacao dos pais que ganharam os Torneios
	pv = 0.9
	i = 0
	while i < tam_pop:
		p1 = random.randrange(0, tam_pop)
		p2 = random.randrange(0, tam_pop)
		while p1 == p2:
			p2 = random.randrange(0, tam_pop)
		chance = random.random()
		if((populacao[p1].fitness > populacao[p2].fitness and chance >= pv) or populacao[p1].fitness < populacao[p2].fitness and chance < pv):
			#como é um problema de minimização quando o fitness do primeiro pai for MAIOR, a chance gerada aleatóriamente precisa, também, ser
			#MAIOR do que o valor pré definido (ou seja, a chance desse cara com fitness maior ser escolhido é MENOR)
			#caso o fitness seja MENOR, então ele tem 90% de chance de ser escolhido ja que 90% dos números entre 0 e 1 são MENORE que 0.9
			pais_vencedores.append(p1)
		else:
			pais_vencedores.append(p2)
		
		i+=1
		
	return pais_vencedores

def Cruzamento(pai1, pai2, populacao, pop_aux):
	#gera dois indivíduos aleatóriamente que serão alterados de acordo com os resultados do Cruzamento
	filho1 = Individuo(dimensao)
	filho2 = Individuo(dimensao)

	#dois pais vão gerar dois filhos onde o PRIMEIRO filho possui os 3 primeiros digitos do pai 1 e os 3 ultimos do pai 2
	#e o SEGUNDO filho possui os 3 primeiros digitos do pai 2 e os 3 ultimos do pai 1
	for i in range(dimensao):
		for j in range(0,3):
			filho1.binario[i-1][j] = populacao[pai1].binario[i-1][j]
			filho2.binario[i-1][j] = populacao[pai2].binario[i-1][j]
		for j in range(3,6):
			filho1.binario[i-1][j] = populacao[pai2].binario[i-1][j]
			filho2.binario[i-1][j] = populacao[pai1].binario[i-1][j]

	pop_aux.append(filho1)
	pop_aux.append(filho2)

def Mutacao(individuo):
	#a mutação vai inverter os dois primeiros digitos de CADA uma das representações binárias do individuo em questão
	for i in range(dimensao):
		if individuo.binario[i][0] == 0:
			individuo.binario[i][0] = 1
		else:
			individuo.binario[i][0] = 0
		
		if individuo.binario[i][1] == 0:
			individuo.binario[i][1] = 1
		else:
			individuo.binario[i][1] = 0

def Elitismo(populacao):
	fitness = 1000
	indice = 0
	for i in range(len(populacao)):
		if populacao[i].fitness < fitness:
			fitness = populacao[i].fitness
			indice = i
	
	return indice

#gera uma população com individuos aleatórios
for i in range(tam_pop):
	populacao.append(Individuo(dimensao))
#calcula o fitness de cada indivíduo
for i in populacao:
	i.fitness = func_obj(RepresentacaoReal(i))
#começa o AG
while atual < geracoes:
	indice_ganhadores = Torneio(populacao)
	#print("ganhadores\n", indice_ganhadores)
	pop_aux = []
	n_cruz = 0
	while n_cruz < len(indice_ganhadores):
		Cruzamento(indice_ganhadores[n_cruz],indice_ganhadores[n_cruz+1], populacao, pop_aux)
		n_cruz+=2

	for i in pop_aux:
		c_mut = random.random()
		if c_mut <= 0.3:
			Mutacao(i)
	elitismo = Elitismo(populacao)
	#A função de elitismo serve para saber o índice do indivíduo com melhor (no caso, menor) fitness
	armazenar = Individuo(dimensao)
	armazenar = populacao[elitismo]
	#gera um individuo auxiliar e temporário para ser armazenado na população "final" da geração, que vai substituir alguém aleatóriamente
	#garantindo que o melhor individuo sempre esteja nas populações futuras
	populacao = pop_aux[:]
	indi_aleatorio = random.randrange(0, len(populacao)-1)
	populacao[indi_aleatorio] = armazenar

	for i in populacao:
		i.fitness = func_obj(RepresentacaoReal(i))
		#print(i.fitness)

	atual += 1

#populacao[0].binario[0] = [0,0,0,0,0,1]
#populacao[0].fitness = func_obj(RepresentacaoReal(populacao[0]))


for i in range(len(populacao)):
	media = media + populacao[i].fitness

media = media/len(populacao)

print("Media: ",media)