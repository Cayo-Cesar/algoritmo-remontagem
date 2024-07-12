def read_data():
    with open('2/input.txt', 'r') as file:
        kmers = file.readline().strip().split(',')
    return kmers

def best_sobreposition(genome, kmers):
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

def assembler(kmers):
    genome = kmers.pop(0)
    while kmers:
        best_sobreposition_len, best_kmer_index = best_sobreposition(genome, kmers)
        if best_sobreposition_len > 0:
            if genome.endswith(kmers[best_kmer_index][:best_sobreposition_len]):
                genome += kmers[best_kmer_index][best_sobreposition_len:]
            else:
                genome = kmers[best_kmer_index][:-best_sobreposition_len] + genome
        else:
            genome += kmers[best_kmer_index]
        kmers.pop(best_kmer_index)
    return genome

def write_data(genome):
    with open('2/CayoCardoso.txt', 'w') as file:
        file.write(genome)

def main():
    kmers = read_data()
    genome = assembler(kmers)
    write_data(genome)

if __name__ == '__main__':
    main()
