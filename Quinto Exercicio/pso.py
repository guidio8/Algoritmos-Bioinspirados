import math
import random

class Particula:
    def __init__(self, dimensao):
        self.dimensao = dimensao
        self.posX = [0] * dimensao  # coordinates
        self.distancia = [0] * dimensao
        self.melhorPessoal = [-math.inf] * dimensao  # Best known pos of particle
        self.fitness = 0
        self.vizinho = []

    def inicia_particula(self, limiteInferior, limiteSuperior):
        for i in range(self.dimensao):
            self.posX[i] = random.uniform(limiteInferior, limiteSuperior)

    def update_distancia(self):
        for i in range(self.dimensao):
            self.posX[i] = self.posX[i] + self.distancia[i]




class PSO:
    def __init__(self, fatorDiversificacao, fatorCognitivo, fatorSocial, limites, dimensao):
        self.w = fatorDiversificacao
        self.c1 = fatorCognitivo
        self.c2 = fatorSocial
        self.topology = {}
        self.dimensao = dimensao
        self.limiteInferior = limites[0]
        self.limiteSuperior = limites[1]
        self.melhorGrupo = [self.limiteSuperior] * dimensao

    def arruma_vizinhos(self, cloud_particles):
        for i in range(len(cloud_particles)):
            if i - 1 == -1:
                vizinhos = [len(cloud_particles) - 1, i + 1]
            elif i + 1 >= len(cloud_particles):
                vizinhos = [i - 1, 0]
            else:
                vizinhos = [i - 1, i + 1]
            self.topology[i] = vizinhos
        return self.topology

    def inicia_nuvem(self, qtdParticulas):
        nuvem = []
        for _ in range(qtdParticulas):
            nuvem.append(Particula(self.dimensao))
            nuvem[-1].inicia_particula(self.limiteInferior, self.limiteSuperior)
        return nuvem

    def distancia(self, pij, gj, xij):
        dij = 1
        r1 = random.random()
        r2 = random.random()

        dij += self.w * dij
        dij += self.c1 * r1 * (pij - xij)
        dij += self.c2 * r2 * (gj - xij)

        dij = self.limite_topologico(dij)

        return dij

    def melhor_vizinho(self, nuvem, particula):
        best_fo = math.inf
        melhor_vizinho = []
        for vizinho in particula.vizinho:
            if self.f(nuvem[vizinho].posX) < best_fo:
                best_fo = self.f(nuvem[vizinho].posX)
                melhor_vizinho = nuvem[vizinho].posX
        particula.melhor_pessoal = melhor_vizinho

    def limite_topologico(self, xi):
        if xi >= self.limiteSuperior:
            return self.limiteSuperior
        elif xi <= self.limiteInferior:
            return self.limiteInferior
        else:
            return xi

    def f(self, x):
        """
        7 - Alpine 2 Function
        interval = 0≤ xi ≤ 10.
        minimum =  x∗= (7.917· · ·7.917), f(x∗) = 2.808D ~= 174.617174...
        """
        fo = 0
        for xi in x:
            xi = self.limite_topologico(xi)
            fo += abs(xi * math.sin(xi) + 0.1 * xi)
        return fo

