from collections import defaultdict

class Node:
    # Classe que representa um nó na lista encadeada.
    def __init__(self, value=None):
        self.value = value
        self.next = None

class LinkedList:
    # Classe que representa uma lista encadeada.
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        # Adiciona um novo nó no início da lista.
        new_node = Node(value)
        if not self.head:
            # Se a lista estiver vazia, o novo nó se torna tanto a cabeça quanto a cauda.
            self.head = self.tail = new_node
        else:
            # Caso contrário, insere o novo nó no início da lista.
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        # Remove e retorna o primeiro nó da lista.
        if not self.head:
            return None
        # Salva o valor do nó que está na cabeça.
        value = self.head.value
        # Move a cabeça para o próximo nó.
        self.head = self.head.next
        # Se a lista ficou vazia, também atualiza a cauda para None.
        if not self.head:
            self.tail = None
        return value

    def __iter__(self):
        # Permite a iteração sobre os nós da lista.
        current = self.head
        while current:
            yield current.value
            current = current.next

class DNAAssembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.k = None  # Tamanho dos k-mers
        self.graph = defaultdict(list)  # Grafo de De Bruijn
        self.in_degrees = defaultdict(int)  # Graus de entrada dos nós
        self.out_degrees = defaultdict(int)  # Graus de saída dos nós
        self.genome = ""  # Genoma montado

    def read_data(self):
        # Lê os dados do arquivo de entrada
        with open(self.input_file, 'r') as file:
            kmers_line = file.readline().strip()  # Lê a linha contendo os k-mers
            kmers_list = kmers_line.split(',')  # Separa os k-mers por vírgula
            self.k = len(kmers_list[0])  # Assume que todos os k-mers têm o mesmo tamanho

            # Cria o grafo de De Bruijn
            for kmer in kmers_list:
                prefix = kmer[:-1]  # Prefixo do k-mer
                suffix = kmer[1:]  # Sufixo do k-mer
                self.graph[prefix].append(suffix)  # Adiciona a aresta no grafo
                self.out_degrees[prefix] += 1  # Incrementa o grau de saída do prefixo
                self.in_degrees[suffix] += 1  # Incrementa o grau de entrada do sufixo

    def find_start_node(self):
        # Encontra o nó inicial para começar a montagem do genoma
        start_node = None
        for node in self.graph:
            if self.out_degrees[node] > self.in_degrees[node]:
                # Se o nó tem mais arestas de saída do que de entrada, é um bom candidato a nó inicial
                # Pois é mais provável que seja o início do caminho Euleriano
                return node
            if self.out_degrees[node] == self.in_degrees[node] and start_node is None:
                # Se os graus de entrada e saída são iguais, também pode ser um candidato
                # Neste caso, ele pode ser um candidato, mas nao é retornado de imediato ele é armazenado para ser retornado caso não seja encontrado outro nó
                start_node = node
        return start_node

    def assemble_genome(self):
        # Monta o genoma usando o grafo de De Bruijn
        if not self.graph:
            print("Nenhum kmer disponível para montagem.")
            return

        # Encontra o nó inicial para começar a montagem
        start_node = self.find_start_node()
        if start_node is None:
            print("Não foi possível determinar o nó inicial para a montagem.")
            return

        # Inicializa a pilha e a lista encadeada para armazenar o caminho Euleriano
        stack = [start_node]  # Inicializa a pilha com o nó inicial
        path = LinkedList()  # Lista encadeada para armazenar o caminho Euleriano

        # Realiza a busca em profundidade para montar o caminho Euleriano
        while stack:
            current = stack[-1]  # Obtém o nó no topo da pilha
            if self.graph[current]:
                # Se o nó atual tem vizinhos não visitados, adiciona o próximo nó à pilha
                next_node = self.graph[current].pop()
                stack.append(next_node)
            else:
                # Se todos os vizinhos foram visitados, adiciona o nó atual ao caminho
                path.append(stack.pop())

        self.genome = path.pop()  # Inicializa o genoma com o primeiro nó do caminho
        for node in path:
            self.genome += node[-1]  # Constrói o genoma a partir do caminho

    def write_data(self):
        # Escreve o genoma montado no arquivo de saída
        with open(self.output_file, 'w') as file:
            file.write(self.genome)

    def run(self):
        # Executa o processo completo de montagem do genoma
        self.read_data()
        self.assemble_genome()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/output-question1.txt'
    output_path = 'inputs-outputs/CayoCardoso.txt'
    assembler = DNAAssembler(input_path, output_path)
    assembler.run()
