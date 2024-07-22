class Node:
    #Classe que representa um nó na lista encadeada.
    def __init__(self, value=None):
        self.value = value
        self.next = None

class LinkedList:
    #Classe que representa uma lista encadeada.
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        #Adiciona um novo nó ao final da lista.
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def pop(self):
        #Remove e retorna o primeiro nó da lista.
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return value

    def remove(self, value):
        #Remove um nó da lista com o valor especificado.
        current = self.head
        previous = None
        while current:
            if current.value == value:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                if current == self.tail:
                    self.tail = previous
                return
            previous = current
            current = current.next

    def is_empty(self):
        #Verifica se a lista está vazia.
        return self.head is None

    def __iter__(self):
        #Permite a iteração sobre os nós da lista.
        current = self.head
        while current:
            yield current.value
            current = current.next

class DNAAssembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.kmers = LinkedList()
        self.genome = ""
        self.kmer_dict = {}

    def read_data(self):
        #Lê os kmers do arquivo de entrada e inicializa o dicionário de kmers.
        with open(self.input_file, 'r') as file:
            kmers_line = file.readline().strip()
            kmers_list = kmers_line.split(',')
            for kmer in kmers_list:
                self.kmers.append(kmer)

        # Preenche o dicionário com prefixos e sufixos
        self.kmer_dict = {} # Dicionario que mapeia prefixos e sufixos para kmers
        for kmer in kmers_list: # Para cada kmer, adiciona o prefixo e o sufixo ao dicionário
            prefix = kmer[:-1] 
            suffix = kmer[1:] 
            if prefix not in self.kmer_dict: # Se o prefixo ou o sufixo não estiverem no dicionário, adiciona-os
                self.kmer_dict[prefix] = []
            if suffix not in self.kmer_dict:
                self.kmer_dict[suffix] = []
            self.kmer_dict[prefix].append(kmer) # Adiciona o kmer à lista de kmers associados ao prefixo
            self.kmer_dict[suffix].append(kmer) # Adiciona o kmer à lista de kmers associados ao sufixo

    def best_sobreposition(self, genome):
        #Encontra o kmer que tem a melhor sobreposição com o genoma atual.
        best_sobreposition_len = 0
        best_kmer = None
        k = len(next(iter(self.kmers)))  # Assume que todos os kmers têm o mesmo tamanho

        # Verifica sobreposição com o sufixo do genoma
        suffix = genome[-(k-1):] 
        if suffix in self.kmer_dict: # Se o sufixo estiver no dicionário, verifica a sobreposição com os kmers associados
            for kmer in self.kmer_dict[suffix]: # Para cada kmer associado ao sufixo
                if kmer not in self.kmers: 
                    continue
                sobreposition_len = len(suffix) # Calcula o comprimento da sobreposição
                if genome.endswith(kmer[:sobreposition_len]): # Se o genoma terminar com o sufixo do kmer
                    if sobreposition_len > best_sobreposition_len: # Se a sobreposição for maior que a melhor sobreposição encontrada até agora
                        best_sobreposition_len = sobreposition_len
                        best_kmer = kmer

        # Verifica sobreposição com o prefixo do genoma
        prefix = genome[:k-1]
        if prefix in self.kmer_dict:
            for kmer in self.kmer_dict[prefix]:
                if kmer not in self.kmers:
                    continue
                sobreposition_len = len(prefix)
                if genome.startswith(kmer[-sobreposition_len:]):
                    if sobreposition_len > best_sobreposition_len:
                        best_sobreposition_len = sobreposition_len
                        best_kmer = kmer

        return best_sobreposition_len, best_kmer

    def assembler(self):
        #Montagem do genoma a partir dos kmers usando sobreposição.
        if self.kmers.is_empty():
            raise ValueError("Nenhum kmer disponível para montagem.")
        
        # Inicializa o genoma com um kmer aleatório
        self.genome = self.kmers.pop()
        
        # Enquanto houver kmers disponíveis, tenta adicionar um kmer ao genoma
        while not self.kmers.is_empty():
            # Chama a função best_sobreposition para encontrar o melhor kmer a ser adicionado
            best_sobreposition_len, best_kmer = self.best_sobreposition(self.genome)
            print(f"Melhor comprimento de sobreposição: {best_sobreposition_len}, Melhor kmer: {best_kmer}")

            # Se não houver um kmer válido, adiciona um kmer aleatório ao genoma
            if not best_kmer:
                print("Nenhum kmer válido encontrado")
                self.genome += self.kmers.pop()
            else:
                if best_sobreposition_len > 0:
                    # Adiciona o kmer ao genoma de acordo com a sobreposição
                    if self.genome.endswith(best_kmer[:best_sobreposition_len]):
                        self.genome += best_kmer[best_sobreposition_len:]
                    else:
                        self.genome = best_kmer[:-best_sobreposition_len] + self.genome
                else:
                    self.genome += best_kmer

            # Remove o kmer adicionado da lista de kmers
                self.kmers.remove(best_kmer)

    def write_data(self):
        #Escreve o genoma montado no arquivo de saída.
        with open(self.output_file, 'w') as file:
            file.write(self.genome)

    def run(self):
        #Executa o processo completo de montagem do genoma.
        self.read_data()
        self.assembler()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/output-question1.txt'
    output_path = 'inputs-outputs/CayoCardoso.txt'
    assembler = DNAAssembler(input_path, output_path)
    assembler.run()
