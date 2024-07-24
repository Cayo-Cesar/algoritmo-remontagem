def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    if content1 == content2:
        print("Os arquivos são iguais.")
    else:
        for i, (line1, line2) in enumerate(zip(content1.splitlines(), content2.splitlines())):
            if line1 != line2:
                print(f"Diferença encontrada na linha {i+1}:")
                print(f"Arquivo 1: {line1}")
                print(f"Arquivo 2: {line2}")
                break
        else:
            print("Os arquivos são diferentes, mas possuem o mesmo número de linhas.")

# Exemplo de uso
file1 = 'inputs-outputs/input-question1.txt'
file2 = 'inputs-outputs/CayoCardoso.txt'
compare_files(file1, file2)