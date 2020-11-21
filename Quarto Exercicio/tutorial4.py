import sys
import csv
import os
import random
import math

class Formiga:
    def __init__(self, quantidade_cidades):
        self.caminho = []
        self.quantidade_cidades = quantidade_cidades
    #coloca cada formiga criada em uma cidade aleatoria para começar
    def posicaoInicial(self, quantidade_cidades):
        cidade_inicial = random.randint(0, quantidade_cidades-1)
        self.caminho.append(cidade_inicial)
    
    def visitaCidade(self, indiceCidade):
        self.caminho.append(indiceCidade)
    
    def esvaziarCaminho(self):
        self.caminho = []

    def recomecarFormiga(self, quantidade_cidades):
        self.esvaziarCaminho()
        self.posicaoInicial(quantidade_cidades)

    def verificaSeVisitou(self, indiceCidade):
        if indiceCidade in self.caminho:
            return True
        else:
            return False

    @staticmethod
    def geraPopFormigas(quantidade_formigas):
        populacao = []
        for i in range(quantidade_formigas):
            populacao.append(Formiga(quantidade_formigas))
        return populacao

class AntSystem:
    def __init__(self, alpha, beta, q, evaporacao, arquivoTxt):
        self.alpha = alpha
        self.beta = beta
        self.q = q
        self.evaporacao = evaporacao
        self.feromonio = arquivoTxt['matriz_feromonio']
        self.distancia = arquivoTxt['distancias']
        self.quantidade_cidades = arquivoTxt['quantidade_cidades']
        self.prob = [0] * self.quantidade_cidades
        self.melhor_resultado = math.inf
        self.caminho_otimo = []

    def probabilidadeVisitarCidade(self, ant):
        #decide a probabilidade de visitar cada cidade a partir da cidade atual, que é o último item no vetor de caminho
        cidadeAtual = formiga.caminho[len(formiga.caminho)-1]
        feromoniox = 0

        for j in range(0, self.quantidade_cidades):
            if ((formiga.verificaSeVisitou(j)) == False and self.distancia[cidadeAtual][j] != 0):
                #atualiza caso a cidade não tenha sido visitada e não esteja verificando a cidade atual
                feromoniox += pow(self.feromonio[cidadeAtual][j], self.alpha) * pow(1 / self.distancia[cidadeAtual][j], self.beta)

        for j in range(0, self.quantidade_cidades):
            if formiga.verificaSeVisitou(j):
                #se a cidade ja tiver sido visitada, a probabilidade da formiga visitar ela de novo é 0
                self.prob[j] = 0
            else:
                n = pow(self.feromonio[cidadeAtual][j], self.alpha) * pow(1 / self.distancia[cidadeAtual][j], self.beta)
                self.prob[j] = n / feromoniox

    def gerarCaminho(self, formiga):
        #enquanto a formiga não tiver visitado todas as cidades
        while (len(formiga.caminho) < self.quantidade_cidades):
            cidadeAtual = formiga.caminho[len(formiga.caminho)-1]

            self.probabilidadeVisitarCidade(formiga)
            #achei uma forma de gerar um valor aleatório que leva em consideração "peso"(a probabilidade da cidade ser visitada é o peso dela) na internet
            somatoriaChance = 0

            for i in range(0, self.quantidade_cidades):
                somatoriaChance += self.prob[i]

            #cria um valor aleatorio que leva em consideração que cada cidade possui uma probabilidade de vistia diferente
            biased = random.uniform(0, somatoriaChance)
            aux = 0
            for i in range(0, self.quantidade_cidades):
                aux += self.prob[i]
                #verificar se não é a mesma cidade que a formiga se encontra e se ela também não foi visitada ainda
                if (aux >= biased and self.distancia[cidadeAtual][i] != 0 and formiga.verificaSeVisitou(i) == False):
                    formiga.visitaCidade(i)
                    break
    
    def calculaDistanciaPercorrida(self, caminho):
        distancia = 0
        aux = caminho[0]
        inicial = aux
        final = caminho[len(caminho)-1]
        #faz a somatoria da distancia entre a cidade atual e a proxima, mas não "da a volta"
        for i in caminho:
            distancia += self.distancia[aux][i]
            aux = i
        #soma a distancia da cidade final para a inicial porque o caixeiro volta à cidade inicial no final do percurso
        distancia += self.distancia[final][inicial]
        return distancia

    def resetaMatrizFeromonio(self):
        for i in range(0, self.quantidade_cidades):
            self.feromonio[i] = pow(10, -16)

    def atualizaFeromonio(self, populacao):
        #sempre que o metodo for chamado, haverá uma evaporação dos feromonios de acordo com a taxa dada
        for i in range(0, self.quantidade_cidades):
            for j in range(0, self.quantidade_cidades):
                if self.distancia[i][j] != 0:
                    self.feromonio[i][j] *= self.evaporacao
        #depois da evaporação, adiciona um valor do feromonio depositado durante o percurso de acordo com a função do tutorial
        for formiga in populacao:
            if len(formiga.caminho) > 1:
                feromonio_depositado = self.q/self.calculaDistanciaPercorrida(formiga.caminho)
            else:
                feromonio_depositado = 0

            for i in range(0, len(formiga.caminho)-1):
                self.feromonio[formiga.caminho[i]][formiga.caminho[i+1]] += feromonio_depositado
            self.feromonio[formiga.caminho[len(formiga.caminho)-1]][formiga.caminho[0]] += feromonio_depositado

    def melhorSolucao(self, solucao):
        aux = self.calculaDistanciaPercorrida(solucao)
        if aux < self.melhor_resultado:
            self.melhor_resultado = aux
            self.caminho_otimo = solucao[:]

    def getMelhorSolucao(self):
        return self.melhor_resultado, self.caminho_otimo
    
 #funcao de leitura e escrita em arquivo da Barbara
def read_file(filepath):
    global data
    
    filepath = filepath.rstrip('\n\r')

    data = {'distancias': {}, 'matriz_feromonio': {}, 'quantidade_cidades': 0}

    with open(filepath, 'r') as distancias_file:
        for i, line in enumerate(distancias_file, start=0):
            data['distancias'][i] = list(map(int, line.split()))
            data['matriz_feromonio'][i] = [10 ** -16] * len(line.split())
        data['quantidade_cidades'] = len(data['distancias'])

def write_results(file):
    if os.path.isfile(file):
        with open(file, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(
                {'Quantidade Cidades': data['quantidade_cidades'], 'Resultado': fo_maximo_encontrado, 'Iterations': geracoes,
                 'Evaporation': taxa_evaporacao})
    else:
        with open(file, 'w+', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {'Quantidade Cidades': data['quantidade_cidades'], 'Resultado': fo_maximo_encontrado, 'Iterations': geracoes,
                 'Evaporation': taxa_evaporacao})


#main
read_file(sys.argv[3])
alpha = 1
beta = 5
Q = 100
taxa_evaporacao = float(sys.argv[2])
geracoes = int(sys.argv[1])
atual = 0
colonia = AntSystem(alpha, beta, Q, taxa_evaporacao, data)

populacao = Formiga.geraPopFormigas(data['quantidade_cidades'])
while (atual < geracoes):
    for formiga in populacao:
        formiga.recomecarFormiga(data['quantidade_cidades'])
        colonia.gerarCaminho(formiga)
        colonia.melhorSolucao(formiga.caminho)
    colonia.atualizaFeromonio(populacao)
    atual += 1
colonia.resetaMatrizFeromonio()
fo_maximo_encontrado, solucao_otima_encontrada = colonia.getMelhorSolucao()
print(f"Número de Cidades: {data['quantidade_cidades']} \nSolução: {fo_maximo_encontrado} : {solucao_otima_encontrada}")

fieldnames = ['Quantidade Cidades', 'Resultado', 'Iterations', 'Evaporation']
file = f"{sys.argv[3].replace('.txt', '')}-results.csv"
write_results(file)