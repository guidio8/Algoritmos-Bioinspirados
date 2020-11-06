# coding: utf-8
import math
import numpy as np
import random
import sys
import os

tam_pop = int(sys.argv[3] )
geracoes = int(sys.argv[4])
chance_mutacao = float(sys.argv[1])
taxa_cruzamento = float(sys.argv[2])
execucao = sys.argv[5]
instancia = sys.argv[6]
atual = 1
media = 0.0

os.chdir('valores')
def GerarValoresIniciais(numero):
	os.chdir(numero)
	profits = []
	pesos = []
	solucao = []
	with open("p0" + numero + "_s.txt") as f:
		for line in f:
			solucao.append(int(line.replace('\n', '')))
	with open("p0" + numero +"_c.txt") as f:
		for line in f:
			capacidade = int(line)
	with open("p0" + numero +"_p.txt") as f:
		for line in f:
			profits.append(int(line.replace('\n', '').strip()))
	with open("p0" + numero +"_w.txt") as f:
		for line in f:
			pesos.append(int(line.replace('\n', '').strip()))
	tam_mochila = len(profits)
	return profits, pesos, capacidade, tam_mochila, solucao

def Somatoria(vet_valores, solucao):
	peso_atual = 0
	for i in range(len(solucao)):
		if solucao[i] == 1:
			peso_atual += vet_valores[i]
	return peso_atual

def func_obj(vet_pesos, vet_profit, capacidade, solucao):
	if(Somatoria(vet_pesos, solucao) <= capacidade):
		return Somatoria(vet_profit, solucao)
	else:
		#copiei a funcao que estava no portal
		#return (Somatoria(vet_pesos, solucao) - (Somatoria(vet_pesos, solucao) * (Somatoria(vet_profit, solucao) - capacidade))) 
		return Somatoria(vet_profit, solucao) * (1 - (Somatoria(vet_pesos, solucao) - capacidade) / capacidade)
class Mochila:
	def __init__(self, geracao):
		self.geracao = geracao
		self.binario = GerarIndividuo(tam_mochila)
		self.fitness = 0
#funcao que gera uma representação binária aleatória de 6 dígitos para cada indivíduo
def GerarIndividuo(tam_mochila):
	individuo = []
	for i in range(tam_mochila):
		individuo.append(random.randint(0,1))
	return individuo

def Torneio(populacao):
	pais_vencedores = [] 
	pv = 0.9
	i = 0
	while i < tam_pop:
		p1 = random.randrange(0, tam_pop)
		p2 = random.randrange(0, tam_pop)
		while p1 == p2:
			p2 = random.randrange(0, tam_pop)
		chance = random.random()
		if((populacao[p1].fitness < populacao[p2].fitness and chance >= pv) or populacao[p1].fitness > populacao[p2].fitness and chance < pv):
			pais_vencedores.append(populacao[p1])
		else:
			pais_vencedores.append(populacao[p2])
		
		i+=1
		
	return pais_vencedores

def EscreveArquivo(media, desvio, melhor_fitness, instancia, execucao):
	folder_name = 'tabelas'
	if not os.path.exists(folder_name):
	    os.makedirs(folder_name)
	    os.chdir(folder_name)
	else:
	    os.chdir(folder_name)
	path = ""
	file_name = 'file' + str(instancia) + '.csv'
	f = open(file_name, "+a")
	if(execucao == '1'):
	    f.write(',' + 'Media' + ',' + 'Desvio' + ',' + 'Melhor Fitness' + '\n')
	f.write(str(execucao) + ',' + str(media) + ',' + str(desvio) + ',' + str(melhor_fitness) + '\n')

def Cruzamento(pai1, pai2, populacao, pop_aux):
	cc = random.random()
	filho1 = Mochila(atual)
	filho2 = Mochila(atual)
	if(cc <= taxa_cruzamento):
		pop_aux.append(Mochila(atual))
		for k in range(tam_mochila-3):
			filho1.binario[k] = pai1.binario[k]
			filho2.binario[k] = pai2.binario[k]
		for k in range(tam_mochila-3, tam_mochila):
			filho1.binario[k] = pai2.binario[k]
			filho2.binario[k] = pai1.binario[k]
	pop_aux.append(filho1)
	pop_aux.append(filho2)

def Mutacao(individuo):
	for i in range(len(individuo.binario)):
		chance = random.random()
		if(chance <= chance_mutacao):
			if(individuo.binario[i] == 0):
				individuo.binario[i] == 1
			else:
				individuo.binario[i] == 0
def Elitismo(populacao):
	fitness = -100000
	indice = 0
	for i in range(len(populacao)):
		if populacao[i].fitness > fitness:
			fitness = populacao[i].fitness
			indice = i
	
	return indice

#rodar 1 vez para cada pasta com parametros iniciais diferentes
for pasta in range(1,8):
	populacao = []
	#valores iniciais
	vet_profit = []
	solucao_otima = []
	capacidade = 0
	tam_mochila = 0
	vet_pesos = []
	pop_aux = []

	vet_profit, vet_pesos, capacidade, tam_mochila, solucao_otima = GerarValoresIniciais(str(pasta))

	#gera uma população com individuos aleatórios
	for i in range(tam_pop):
		populacao.append(Mochila(atual))
	#calcula o fitness de cada indivíduo
	for i in populacao:
		i.fitness = func_obj(vet_pesos, vet_profit, capacidade, i.binario)
	#começa o AG
	while atual < geracoes:
		pais_ganhadores = Torneio(populacao)
		#print("ganhadores\n", pais_ganhadores)
		pop_aux = []
		n_cruz = 0
		while n_cruz < len(pais_ganhadores):
			Cruzamento(pais_ganhadores[n_cruz],pais_ganhadores[n_cruz+1], populacao, pop_aux)
			n_cruz+=2

		for i in pop_aux:
			Mutacao(i)
		
		elitismo = Elitismo(populacao)
		#A função de elitismo serve para saber o índice do indivíduo com melhor (no caso, menor) fitness
		armazenar = Mochila(atual)
		armazenar = populacao[elitismo]
		#gera um individuo auxiliar e temporário para ser armazenado na população "final" da geração, que vai substituir alguém aleatóriamente
		#garantindo que o melhor individuo sempre esteja nas populações futuras
		populacao = pop_aux[:]
		indi_aleatorio = random.randrange(0, len(populacao)-1)
		populacao[indi_aleatorio] = armazenar

		for i in populacao:
			i.fitness = func_obj(vet_pesos, vet_profit, capacidade, i.binario)
			#print(i.fitness)

		atual += 1

	vetor_fitness = []

	for i in populacao:
		vetor_fitness.append(i.fitness)
		#print(i.fitness)

	melhor_fitness = max(vetor_fitness)
	media = np.mean(vetor_fitness)
	desvio = np.std(vetor_fitness)

	#print(melhor_fitness)
	#print(media)
	#print(desvio)
	EscreveArquivo(media, desvio, melhor_fitness, instancia, execucao)
	#retornando para o diretorio "valores" para utilizar a proxima pasta com valores iniciais
	os.chdir('..')
	os.chdir('..')
