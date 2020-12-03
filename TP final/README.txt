Para executar o código é preciso, primeiramente definir alguns parâmetros:
	Tipo de entrada de texto: 
		0 = O algoritmo consegue transformar 2 tipos de arquivos de entrada em grafos, ou uma matriz biária representando um grafo direcionado, ou seja caso i = j 			Elemento(i,j) = 0 (olhar Matriz.txt para ver um exemplo)
		1 = Também é possível ler um arquivo de entrada onde cada linha representa uma aresta com seus extremos separados por uespaço(ver Dolphins.txt para exemplo)
	Tipo de resolução:
		0 = É usado o 0 quando deseja encontrar os K vértices mais influentes na network
		1 = Utiliza o 1 quando se tem uma lista pré-definida de vértices e deseja saber a influência destes na network, neste caso é necessário um arquivo de texto com 		cada elemento da lista em uma linha (ver arqSeed.txt para exemplo)
	Parametro 3: (Valor de K OU arquivo de seeds):
		Este parâmetro depende do anterior, caso tipo de resolução == 0 este parâmetro deve ser um número inteiro de 1 até quantidade de vértices, caso tipo de 
		resolução == 1 deve ser passado o nome do arquivo de entrada com as sementes
	Social network:
		Nome do arquivo que representa a network, levando em consideração o valor passado em "tipo de entrada de texto"
	Tamanho do Grafo:
		Quantidade de vértices(indivíduos) na network
	Probabilidade:
		Valor numérico (float) que representa a probabilidade de cada indivíduo ser "ativado" por algum de seus vizinhos

a linha de comando seria então:

python CalcInfluence.py (Tipo de entrada de texto) (Tipo de resolução) (Parametro 3) (Social Network) (Tamanho do Grafo) (Probabilidade)
	
