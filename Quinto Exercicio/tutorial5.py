
import os
import csv
import sys

from pso import PSO

if __name__ == '__main__':
    w = float(sys.argv[1])
    c_1 = float(sys.argv[2])
    c_2 = float(sys.argv[2])
    dimensao = int  (sys.argv[3])
    m = int(sys.argv[4])
    iteracoes = int(sys.argv[5])
    atual = 0

    pso = PSO(w, c_1, c_2, [-10, 10], dimensao)
    nuvemParticulas = pso.inicia_nuvem(m)
    topology = pso.arruma_vizinhos(nuvemParticulas)

    for i, particula in enumerate(nuvemParticulas, start=0):
        particula.inicia_particula(pso.limiteSuperior, pso.limiteInferior)
        particula.vizinho = topology[i]
        pso.melhor_vizinho(nuvemParticulas, particula)
        
    while atual < iteracoes:
        for i, particula in enumerate(nuvemParticulas, start=0):
            if pso.f(particula.posX) < pso.f(particula.melhorPessoal):
                particula.melhorPessoal = particula.posX[:]
                if pso.f(particula.posX) < pso.f(pso.melhorGrupo):
                    pso.melhorGrupo = particula.posX[:]
            for j in range(particula.dimensao):
                pij = particula.melhorPessoal[j]
                gj = pso.melhorGrupo[j]
                xij = particula.posX[j]
                particula.distancia[j] = pso.distancia(pij, gj, xij)
            particula.update_distancia()
        atual += 1
    profit = pso.f(pso.melhorGrupo)

    file = 'result.csv'
    fieldnames = ['dimensao', 'qtdParticulas', 'iteracoes', 'fatorDiversidade', 'cognitivo_socialFatores', 'profit']
    if os.path.isfile(file):
        with open(file, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(
                {'dimensao': dimensao, 'qtdParticulas': m, 'iteracoes': iteracoes,
                 'fatorDiversidade': w, 'cognitivo_socialFatores': c_2, 'profit': profit})
    else:
        with open(file, 'a+', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {'dimensao': dimensao, 'qtdParticulas': m, 'iteracoes': iteracoes,
                 'fatorDiversidade': w, 'cognitivo_socialFatores': c_2, 'profit': profit})
