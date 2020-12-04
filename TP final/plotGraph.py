import matplotlib.pyplot as plt


x1 = [5, 15, 30]
y1 = [8.07, 22.7, 38.1]

plt.plot(x1, y1, label = "Tempo por Tamanho de Seed")

x2 = [5, 15, 30]
y2 = [13.16, 23.14, 33.31]

plt.plot(x2, y2, label = "Tamanho Seed por Influência")

# plt.xlabel('Tamanho Solução')
# plt.ylabel('Tempo de Execução em segundos')

plt.title("Karate Network")
plt.legend()

plt.show()