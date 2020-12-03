# coding: utf-8
import math
import numpy as np
import random
import sys
import os
import re

sys.setrecursionlimit(15000)

class Vertice:
    #Cada vertice tem um vetor para saber quem são seus vizinhos e seu status
    def __init__(self, qtdVertices):
        self.qtdVertices = qtdVertices
        self.vizinhos = []
        self.status = "inativo"

#função que ativa as arestas do grafo e verifica se o vértice foi ativado também
def flipar(grafo, indice, qtdVertices):
    for i in range(qtdVertices):
        #toda aresta existente começa com valor 1, caso ela tenha sido ativada com sucesso se transforma em 2, caso contrario 3
        if(grafo[indice].vizinhos[i] == 1):
            result = random.uniform(0, 1)
            #primeiramente tenta ativar a aresta do vizinho em questão
            if(result > float(sys.argv[6])):
                #caso a aresta tenha sido ativada, verifica se é um vertice inativo
                if(grafo[i].status == "inativo"):
                    #ativa as arestas de acordo com a probabilidade dada como parâmetro
                    grafo[indice].vizinhos[i] = 2
                    grafo[i].status = "ativo"
                    #função recursiva pois para cada vértice ativado, tenta ativar TODOS os seus vizinhos e vizinhos de vizinhos
                    flipar(grafo, i, qtdVertices)
            else:
                #caso a aresta tenha falhado em sua ativação, anota no grafo só para ter controle de arestas ativas e inativas
                grafo[indice].vizinhos[i] = 3

#ler or arquivos e transformar em um grafo
def read_file(tipoArquivo, tamanhoGrafo):
    global data
    global grafo
    grafo = []
    filepath = sys.argv[4]

    data = {}
    if(tipoArquivo == 0):
        with open(filepath, 'r') as arquivo:
            for i, line in enumerate(arquivo, start = 0):
                #data[i] = list(map(int, re.findall(r'\d', line)))
                data[i] = line.split()
                data[i] = re.findall('\d', data[i])
                print(data[i])

        for i in range(tamanhoGrafo):
            grafo.append(Vertice(tamanhoGrafo))
            grafo[i].vizinhos = data[i]

    if(tipoArquivo == 1):
        for i in range(tamanhoGrafo):
            grafo.append(Vertice(tamanhoGrafo))

        for i in grafo:
            for j in range(tamanhoGrafo):
                i.vizinhos.append(0)

        with open(filepath, 'r') as arquivo:
            for i, line in enumerate (arquivo, start = 0):
                data[i] = line.split()
                x = int(data[i][0])
                y = int(data[i][1])
                grafo[x].vizinhos[y] = 1


#contador para saber quantas arestas estão ativadas no final de cada iteração
def calcular_expectativa(contador, listaSeed):
    for i in listaSeed:
        grafo[i].status = "ativo"

    for i in listaSeed:
        flipar(grafo, i, tamanhoGrafo)
    for i in grafo:
        if i.status == "ativo":
            contador+=1

    return contador

def calcular_solucao(qtdIteracoes, listaSeed):
    aux = 0
    #Como os resultados são baseados na probabilidade de ativação eles vão ser sempre diferentes então realiza N iterações para ter
    #uma média de resultados que acaba sendo mais preciso
    for i in range(qtdIteracoes):
        aux += calcular_expectativa(0, listaSeed)
        read_file(1, tamanhoGrafo)

    aux = aux/qtdIteracoes
    return aux

#transforma o arquivo de sementes iniciais em uma lista
def read_arq_seed(arqSeed, listaSeed):
    global data
    data = []
    filepath = arqSeed

    with open(filepath, 'r') as arquivo:
            for i, line in enumerate (arquivo, start = 0):
                x = line.split()
                listaSeed.append(int(x[0]))

tamanhoGrafo = int(sys.argv[5])
read_file(int(sys.argv[1]), tamanhoGrafo)
tipo = int(sys.argv[2])
listaSeed = []
if(tipo == 0):
    tamMaxSeed = int(sys.argv[3])
elif(tipo == 1):
    arqSeed = sys.argv[3]
    read_arq_seed(arqSeed, listaSeed)
solucao = 0
k = 0
#caso esteja usando o método de encontrar os K vértices mais influentes
if(tipo == 0):
    while(k < tamMaxSeed):
        for i in range(tamanhoGrafo):
            if i not in listaSeed:
                listaSeed.append(i)
                aux = calcular_solucao(100, listaSeed)
                if aux > solucao:
                    solucao = aux
                    melhorVertice = i
                listaSeed.remove(i)
        if melhorVertice not in listaSeed:   
            listaSeed.append(melhorVertice)
            k +=1
#caso esteja usando o método de encontrar a influência dos vértices semente pré-definidos
elif(tipo == 1):
    solucao = calcular_solucao(100, listaSeed)

print("Solucao: ", solucao, "Lista Seed: ", listaSeed)