from collections import deque

class DNAAssembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.kmers = deque()
        self.genome = ""
        self.kmer_dict = {}

    def read_data(self):
        with open(self.input_file, 'r') as file:
            self.kmers = deque(file.readline().strip().split(','))

        for kmer in self.kmers:
            prefix = kmer[:-1]
            suffix = kmer[1:]
            if prefix not in self.kmer_dict:
                self.kmer_dict[prefix] = []
            if suffix not in self.kmer_dict:
                self.kmer_dict[suffix] = []
            self.kmer_dict[prefix].append(kmer)
            self.kmer_dict[suffix].append(kmer)

    def best_overlap(self, genome):
        best_overlap_len = 0
        best_kmer = None
        k = len(self.kmers[0])

        suffix = genome[-(k-1):]
        if suffix in self.kmer_dict:
            for kmer in self.kmer_dict[suffix]:
                overlap_len = len(suffix)
                if kmer not in self.kmers:
                    continue
                if genome.endswith(kmer[:overlap_len]):
                    if overlap_len > best_overlap_len:
                        best_overlap_len = overlap_len
                        best_kmer = kmer

        prefix = genome[:k-1]
        if prefix in self.kmer_dict:
            for kmer in self.kmer_dict[prefix]:
                overlap_len = len(prefix)
                if kmer not in self.kmers:
                    continue
                if genome.startswith(kmer[-overlap_len:]):
                    if overlap_len > best_overlap_len:
                        best_overlap_len = overlap_len
                        best_kmer = kmer

        return best_overlap_len, best_kmer

    def assembler(self):
        self.genome = self.kmers.popleft()
        while self.kmers:
            best_overlap_len, best_kmer = self.best_overlap(self.genome)
            print(f"Best overlap length: {best_overlap_len}, Best kmer: {best_kmer}")

            if not best_kmer:
                print("No valid kmer found")
                self.genome += self.kmers.popleft()
            else:
                if best_overlap_len > 0:
                    if self.genome.endswith(best_kmer[:best_overlap_len]):
                        self.genome += best_kmer[best_overlap_len:]
                    else:
                        self.genome = best_kmer[:-best_overlap_len] + self.genome
                else:
                    self.genome += best_kmer

                self.kmers.remove(best_kmer)

    def write_data(self):
        with open(self.output_file, 'w') as file:
            file.write(self.genome)

    def run(self):
        self.read_data()
        self.assembler()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/output-question1.txt'
    output_path = 'inputs-outputs/CayoCardoso.txt'
    assembler = DNAAssembler(input_path, output_path)
    assembler.run()
