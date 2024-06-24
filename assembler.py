def read_data():
    with open('output.txt', 'r') as file:
        kmers = file.readline().strip().split(',')
    return kmers

def assembler(kmers):
    genome = kmers[0]
    k = len(kmers[0])
    for i in range(1, len(kmers)):
        genome += kmers[i][-k]
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