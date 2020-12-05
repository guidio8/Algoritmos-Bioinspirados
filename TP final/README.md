# Influence Maximization

## Grupo

- Luccas Guidio

## Dependências

- Versão do Python: `3.8`

## Execução

    ~$ python CalcInfluence.py [Tipo de entrada de texto] [Tipo de resolução] [Parametro 3] [Social Network] [Tamanho do Grafo] [Probabilidade]

## Formato do arquivo de instância

#### Tipo de entrada de texto: 
    0 = O algoritmo consegue transformar 2 tipos de arquivos de entrada em grafos,
    ou uma matriz biária representando um grafo direcionado, ou seja caso i = j
    Elemento(i,j) = 0 (Exemplo Matriz.txt)

    1 = Também é possível ler um arquivo de entrada onde cada linha representa uma
    aresta com seus extremos separados por um espaço(Exemplo List.txt)

#### Tipo de resolução:
    0 = É usado o 0 quando deseja encontrar os K vértices mais influentes na network
    1 = Utiliza o 1 quando se tem uma lista pré-definida de vértices e deseja saber a influência destes na network.
    Neste caso é necessário um arquivo de texto com cada elemento da lista em uma linha (Exemplo arqSeed.txt)

#### Parametro 3: (Valor de K OU arquivo de seeds):
    Este parâmetro depende do anterior, caso tipo de resolução == 0 este parâmetro
    deve ser um número inteiro de 1 até quantidade de vértices, caso tipo de
    resolução == 1 deve ser passado o nome do arquivo de entrada com as sementes

#### Social network:
		Nome do arquivo que representa a network, levando em consideração o valor
        passado em "tipo de entrada de texto"

#### Tamanho do Grafo:
        Quantidade de vértices(indivíduos) na network
        
#### Probabilidade:
		Valor numérico (float) que representa a probabilidade de cada indivíduo NÃO ser
        "ativado" por algum de seus vizinhos (Probabilidade de sucesso = (1 - parâmetro dado))


Este é o arquivo Matriz.txt, este arquivo não é
uma instância, é apenas um exemplo. 

    [0, 0, 0, 0, 1]
    [1, 0, 1, 0, 0]
    [0, 0, 0, 0, 0]
    [1, 1, 1, 0, 1]
    [0, 0, 0, 1, 0]

Este é o arquivo Lista.txt, este arquivo não é
uma instância, é apenas um exemplo. 

    0 9
    10 7
    11 2
    5 6
    5 7
    5 9
    3 2

Este é o arquivo arqSeed.txt, este arquivo não é
uma instância, é apenas um exemplo. 

    9
    7
    6
    5
    10





