# ─── Exercício 1: Matriz identidade 5x5 ───
matriz = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

for linha in range(5):
    for coluna in range(5):
        if linha == coluna:
            matriz[linha][coluna] = 1

for linha in range(5):
    print(matriz[linha])


# ─── Exercício 2: Maior valor e posição ───
matriz = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

for linha in range(4):
    for coluna in range(4):
        matriz[linha][coluna] = int(input(f"[{linha}][{coluna}]: "))

print("\nMatriz:")
for linha in range(4):
    print(matriz[linha])

maior    = matriz[0][0]
maior_lin = 0
maior_col = 0

for linha in range(4):
    for coluna in range(4):
        if matriz[linha][coluna] > maior:
            maior     = matriz[linha][coluna]
            maior_lin = linha
            maior_col = coluna

print(f"\nMaior valor: {maior}")
print(f"Linha: {maior_lin}, Coluna: {maior_col}")


# ─── Exercício 3: Controle de alunos ───
alunos = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

for linha in range(5):
    print(f"\nAluno {linha + 1}:")
    alunos[linha][0] = int(input("  Matrícula: "))
    alunos[linha][1] = int(input("  Média das provas: "))
    alunos[linha][2] = int(input("  Média dos trabalhos: "))
    alunos[linha][3] = alunos[linha][1] + alunos[linha][2]

print("\nMatrícula | Med.Provas | Med.Trabalhos | Nota Final")
for linha in range(5):
    print(alunos[linha])

maior_nota = alunos[0][3]
maior_lin  = 0

for linha in range(5):
    if alunos[linha][3] > maior_nota:
        maior_nota = alunos[linha][3]
        maior_lin  = linha

print(f"\nMatrícula do aluno com maior nota: {alunos[maior_lin][0]}")
print(f"Nota final: {maior_nota}")