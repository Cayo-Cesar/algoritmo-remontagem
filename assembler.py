def read_data():
    with open('output.txt', 'r') as file:
        kmers = file.readline().strip().split(',')
    return kmers

def find_best_overlap(genome, kmers):
    best_overlap_len = 0
    best_kmer_index = -1
    k = len(kmers[0])
    
    for i, kmer in enumerate(kmers):
        for j in range(k - 1, 0, -1):
            if genome.endswith(kmer[:j]):
                if j > best_overlap_len:
                    best_overlap_len = j
                    best_kmer_index = i
                break
            elif genome.startswith(kmer[-j:]):
                if j > best_overlap_len:
                    best_overlap_len = j
                    best_kmer_index = i
                break

    return best_overlap_len, best_kmer_index

def assembler(kmers):
    genome = kmers.pop(0)
    while kmers:
        best_overlap_len, best_kmer_index = find_best_overlap(genome, kmers)
        if best_overlap_len > 0:
            if genome.endswith(kmers[best_kmer_index][:best_overlap_len]):
                genome += kmers[best_kmer_index][best_overlap_len:]
            else:
                genome = kmers[best_kmer_index][:-best_overlap_len] + genome
        else:
            genome += kmers[best_kmer_index]
        kmers.pop(best_kmer_index)
    return genome

def write_data(genome):
    with open('CayoCardoso.txt', 'w') as file:
        file.write(genome)

def main():
    kmers = read_data()
    genome = assembler(kmers)
    write_data(genome)

if __name__ == '__main__':
    main()
