class KmerGenerator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = ""
        self.k = 0
        self.kmers = []

    def read_data(self):
        with open(self.input_file, 'r') as file:
            self.data = file.readline().strip()
            self.k = int(file.readline().strip())

    def generate_kmers(self):
        self.kmers = [self.data[i:i+self.k] for i in range(len(self.data) - self.k + 1)]
        self.kmers.sort()

    def write_data(self):
        with open(self.output_file, 'w') as file:
            file.write(','.join(self.kmers))

    def run(self):
        self.read_data()
        self.generate_kmers()
        self.write_data()

if __name__ == '__main__':
    input_path = 'inputs-outputs/input-question1.txt'  # Ajuste o caminho conforme necessário
    output_path = 'inputs-outputs/output-question1.txt'  # Ajuste o caminho conforme necessário
    generator = KmerGenerator(input_path, output_path)
    generator.run()