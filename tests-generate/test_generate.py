import random

def generate_dna_sequence(length):
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choices(bases, k=length))

dna_sequence = generate_dna_sequence(1000000)

with open("tests-generate/dna_sequence.txt", "w") as file:
    file.write(dna_sequence)

print("Sequência de DNA gerada e salva em 'dna_sequence.txt'")
