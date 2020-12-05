import matplotlib.pyplot as plt
filepath = "teste.txt"
data = []
x1 = []
y1 = []
with open(filepath, 'r') as arquivo:
    for i, line in enumerate (arquivo, start = 0):
        data[i] = line.split()
        x1.append(int(data[i][0]))
        y1.append(int(data[i][1]))


plt.plot(x1, y1, label = "Tempo por Tamanho de Seed")


# plt.xlabel('Tamanho Solução')
# plt.ylabel('Tempo de Execução em segundos')

plt.title("Karate Network")
plt.legend()

plt.show()