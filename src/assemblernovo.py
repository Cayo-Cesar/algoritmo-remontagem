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
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        # Remove e retorna o primeiro nó da lista.
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
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
        self.k = None
        self.graph = defaultdict(list)
        self.in_degrees = defaultdict(int)
        self.out_degrees = defaultdict(int)
        self.genome = ""

    def read_data(self):
        with open(self.input_file, 'r') as file:
            kmers_line = file.readline().strip()
            kmers_list = kmers_line.split(',')
            self.k = len(kmers_list[0])  # Assumes all kmers are of the same length

            for kmer in kmers_list:
                prefix = kmer[:-1]
                suffix = kmer[1:]
                self.graph[prefix].append(suffix)
                self.out_degrees[prefix] += 1
                self.in_degrees[suffix] += 1

    def find_start_node(self):
        start_node = None
        for node in self.graph:
            if self.out_degrees[node] > self.in_degrees[node]:
                return node
            if self.out_degrees[node] == self.in_degrees[node] and start_node is None:
                start_node = node
        return start_node

    def assemble_genome(self):
        if not self.graph:
            raise ValueError("Nenhum kmer disponível para montagem.")

        start_node = self.find_start_node()
        if start_node is None:
            raise ValueError("Não foi possível determinar o nó inicial para a montagem.")

        stack = [start_node]
        path = LinkedList()

        while stack:
            current = stack[-1]
            if self.graph[current]:
                next_node = self.graph[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())

        self.genome = path.pop()
        for node in path:
            self.genome += node[-1]

    def write_data(self):
        with open(self.output_file, 'w') as file:
            file.write(self.genome)

    def run(self):
        self.read_data()
        self.assemble_genome()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/output-question1.txt'
    output_path = 'inputs-outputs/CayoCardoso.txt'
    assembler = DNAAssembler(input_path, output_path)
    assembler.run()
