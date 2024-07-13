class DNAAssembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.kmers = []
        self.genome = ""

    # Read data from input file
    def read_data(self):
        with open(self.input_file, 'r') as file:
            self.kmers = file.readline().strip().split(',')

    # Find the best sobreposition between the genome and the kmers
    def best_sobreposition(self, genome, kmers):
        best_sobreposition_len = 0
        best_kmer_index = -1
        k = len(kmers[0])
        
        for i, kmer in enumerate(kmers):
            for j in range(k - 1, 0, -1):
                if genome.endswith(kmer[:j]):
                    if j > best_sobreposition_len:
                        best_sobreposition_len = j
                        best_kmer_index = i
                    break
                elif genome.startswith(kmer[-j:]):
                    if j > best_sobreposition_len:
                        best_sobreposition_len = j
                        best_kmer_index = i
                    break

        return best_sobreposition_len, best_kmer_index
    
    # Assemble the genome from the kmers
    def assembler(self):
        self.genome = self.kmers.pop(0)
        while self.kmers:
            best_sobreposition_len, best_kmer_index = self.best_sobreposition(self.genome, self.kmers)
            print(f"Best sobreposition length: {best_sobreposition_len}, Best kmer index: {best_kmer_index}")
            
            if best_kmer_index == -1:
                print("No valid k-mer found, appending the next k-mer.")
                self.genome += self.kmers.pop(0)
            else:
                if best_sobreposition_len > 0:
                    if self.genome.endswith(self.kmers[best_kmer_index][:best_sobreposition_len]):
                        self.genome += self.kmers[best_kmer_index][best_sobreposition_len:]
                    else:
                        self.genome = self.kmers[best_kmer_index][:-best_sobreposition_len] + self.genome
                else:
                    self.genome += self.kmers[best_kmer_index]
                self.kmers.pop(best_kmer_index)

    # Write the genome to output file
    def write_data(self):
        with open(self.output_file, 'w') as file:
            file.write(self.genome)

    # Run the assembler
    def run(self):
        self.read_data()
        self.assembler()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/output-question1.txt'  
    output_path = 'inputs-outputs/CayoCardoso.txt'  
    assembler = DNAAssembler(input_path, output_path)
    assembler.run()
