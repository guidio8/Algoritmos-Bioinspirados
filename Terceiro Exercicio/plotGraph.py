import matplotlib.pyplot as plt
filepath = "teste.txt"
data = {}
x1 = []
y1 = []
with open(filepath, 'r') as arquivo:
    for i, line in enumerate (arquivo, start = 0):
        data[i] = line.split(",")
        x1.append(float(data[i][2]))
        y1.append(float(data[i][1]))


plt.plot(x1, y1)


plt.xlabel('Tamanho Solução')
plt.ylabel('Tempo de Execução')

plt.title("Livros Politicos Network")
plt.legend()

plt.show()