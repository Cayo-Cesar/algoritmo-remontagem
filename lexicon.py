# Descrição: Dado uma string e um inteiro k, retorna todos os k-mers da string ordenados lexicograficamente.

'''
Exemplo de input: 

ACGTACGT
3
'''

def read_data():
    with open('input.txt', 'r') as file:
        data = file.readline().strip()
        k = int(file.readline().strip()) 
    return data, k

def generate_kmers(data, k):
    kmers = []
    for i in range(len(data)-k+1):
        kmers.append(data[i:i+k])
    kmers.sort()
    return kmers

def write_data(kmers):
    with open('output.txt', 'w') as file:
        file.write(','.join(kmers))

def main():
    data, k = read_data()
    kmers = generate_kmers(data, k)
    write_data(kmers)

if __name__ == '__main__':
    main()
