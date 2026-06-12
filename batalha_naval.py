import random
#alguem podia passar pro main mas ta bom assim
# tabuleiro 10x10
LINHAS = 10
COLUNAS = 10
LETRAS = ['A','B','C','D','E','F','G','H','I','J']

# cria matriz vazia com zeros
def criar_tabuleiro():
    tabuleiro = []
    for i in range(LINHAS):
        linha = []
        for j in range(COLUNAS):
            linha.append('.')
        tabuleiro.append(linha)
    return tabuleiro

# colocando o tabuleiro na tela
def mostrar_tabuleiro(tabuleiro, nome):
    print("\nTabuleiro do " + nome)
    print("    0  1  2  3  4  5  6  7  8  9")
    for i in range(LINHAS):
        linha_str = " " + LETRAS[i] + "  "
        for j in range(COLUNAS):
            celula = tabuleiro[i][j]
            if celula == 1:
                linha_str = linha_str + "#  "
            else:
                linha_str = linha_str + str(celula) + "  "
        print(linha_str)

# conta quantos navios ainda estao vivos (oculto usa 1 pra marcar navio)
def contar_navios(tabuleiro):
    total = 0
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if tabuleiro[i][j] == 1:
                total = total + 1
    return total
#Victor codou esses loops!
# Loop de A-J
def ler_linha(mensagem):
    while True:
        letra = input(mensagem).upper().strip()
        if letra in LETRAS:
            return LETRAS.index(letra)
        print("Linha invalida! Digite uma letra de A ate J.")

# loop se nao for de 0 a 9 ou nao for numero
def ler_coluna(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and 0 <= int(entrada) <= 9:
            return int(entrada)
        print("Coluna invalida! Digite um numero de 0 ate 9.")

# H ou V ate acertar
def ler_direcao(mensagem):
    while True:
        direcao = input(mensagem).upper().strip()
        if direcao in ('H', 'V'):
            return direcao
        print("Direcao invalida! Use H para horizontal ou V para vertical.")

# jogador escolhe onde colocar os navios
def posicionar_jogador(tabuleiro):
    navios = [
        ("Porta-avioes",      5),
        ("Navio-tanque",      4),
        ("Contratorpedeiro",  3),
        ("Submarino",         2),
        ("Destroier",         1),
    ]
    print("\nPosicione seus navios no tabuleiro")
    print("Linhas: A ate J  |  Colunas: 0 ate 9  |  Direcao: H ou V")

    for navio, tamanho in navios:
        posicionado = False
        while not posicionado:
            print(f"\n[{navio}, tamanho: {tamanho}]")
            mostrar_tabuleiro(tabuleiro, "Jogador")

            linha  = ler_linha("Linha inicial (A-J): ")
            coluna = ler_coluna("Coluna inicial (0-9): ")
            direcao = ler_direcao("Direcao (H/V): ")

            # verifica se o navio cabe e nao tem colisao
            cabe = True
            for k in range(tamanho):
                if direcao == 'H':
                    if coluna + k > 9:
                        cabe = False
                        break
                    elif tabuleiro[linha][coluna + k] != '.':
                        cabe = False
                        break
                else:
                    if linha + k > 9:
                        cabe = False
                        break
                    elif tabuleiro[linha + k][coluna] != '.':
                        cabe = False
                        break

            if not cabe:
                print("Nao cabe ai! Tente outra posicao.")
            else:
                for k in range(tamanho):
                    if direcao == 'H':
                        tabuleiro[linha][coluna + k] = 1
                    else:
                        tabuleiro[linha + k][coluna] = 1
                posicionado = True

# computador coloca os navios de forma aleatoria
def posicionar_computador(tabuleiro):
    navios = [
        ("Porta-avioes",      5),
        ("Navio-tanque",      4),
        ("Contratorpedeiro",  3),
        ("Submarino",         2),
        ("Destroier",         1),
    ]

    for navio, tamanho in navios:
        posicionado = False
        while not posicionado:
            linha   = random.randint(0, 9)
            coluna  = random.randint(0, 9)
            direcao = random.choice(['H', 'V'])

            cabe = True
            for k in range(tamanho):
                if direcao == 'H':
                    if coluna + k > 9 or tabuleiro[linha][coluna + k] != '.':
                        cabe = False
                        break
                else:
                    if linha + k > 9 or tabuleiro[linha + k][coluna] != '.':
                        cabe = False
                        break

            if cabe:
                for k in range(tamanho):
                    if direcao == 'H':
                        tabuleiro[linha][coluna + k] = 1
                    else:
                        tabuleiro[linha + k][coluna] = 1
                posicionado = True

# jogador ataca — repete o turno se a coordenada ja foi atacada
def atacar_jogador(oculto_computador, visivel_computador):
    while True:
        linha  = ler_linha("\nQual linha quer atacar? (A-J): ")
        coluna = ler_coluna("Qual coluna quer atacar? (0-9): ")

        celula = visivel_computador[linha][coluna]
        if celula == 'X' or celula == 'O':
            print("Voce ja atacou esse lugar! Escolha outra coordenada.")
        else:
            break

    if oculto_computador[linha][coluna] == 1:
        oculto_computador[linha][coluna] = 0
        visivel_computador[linha][coluna] = 'X'
        print("Acertou!")
        print("Navios inimigos restantes: " + str(contar_navios(oculto_computador)))
    else:
        visivel_computador[linha][coluna] = 'O'
        print("Errou!")

# computador ataca
def atacar_computador(oculto_jogador, visivel_jogador, ja_atacados):
    while True:
        linha  = random.randint(0, 9)
        coluna = random.randint(0, 9)
        if [linha, coluna] not in ja_atacados:
            ja_atacados.append([linha, coluna])
            break

    print("Computador atacou: " + LETRAS[linha] + str(coluna))

    if oculto_jogador[linha][coluna] == 1:
        oculto_jogador[linha][coluna] = 0
        visivel_jogador[linha][coluna] = 'X'
        print("Computador acertou um dos seus navios!")
        print("Seus navios restantes: " + str(contar_navios(oculto_jogador)))
    else:
        visivel_jogador[linha][coluna] = 'O'
        print("Computador errou!")

# ------- jogo principal -------

print("----------------------------------")
print("Bem vindo ao Batalha Naval!")
print("----------------------------------")

# cria os 4 tabuleiros
oculto_computador  = criar_tabuleiro()
oculto_jogador     = criar_tabuleiro()
visivel_computador = criar_tabuleiro()
visivel_jogador    = criar_tabuleiro()

# posiciona os navios
posicionar_computador(oculto_computador)
posicionar_jogador(oculto_jogador)

ja_atacados = []

# mostra os tabuleiros iniciais
mostrar_tabuleiro(visivel_computador, "Computador")
print("Navios restantes: " + str(contar_navios(oculto_computador)))
mostrar_tabuleiro(visivel_jogador, "Jogador")
print("Navios restantes: " + str(contar_navios(oculto_jogador)))

# loop do jogo
while True:

    # turno do jogador
    print("\n--- Sua vez ---")
    atacar_jogador(oculto_computador, visivel_computador)

    mostrar_tabuleiro(visivel_computador, "Computador")
    print("Navios restantes: " + str(contar_navios(oculto_computador)))
    mostrar_tabuleiro(visivel_jogador, "Jogador")
    print("Navios restantes: " + str(contar_navios(oculto_jogador)))

    if contar_navios(oculto_computador) == 0:
        print("\nParabens! Voce afundou todos os navios inimigos!")
        print("Jogo feito por: Vinicius, Victor Hugo, Joao Victor")
        print("Obrigado por jogar!")
        break

    # turno do computador
    print("\n--- Vez do computador ---")
    atacar_computador(oculto_jogador, visivel_jogador, ja_atacados)

    mostrar_tabuleiro(visivel_computador, "Computador")
    print("Navios restantes: " + str(contar_navios(oculto_computador)))
    mostrar_tabuleiro(visivel_jogador, "Jogador")
    print("Navios restantes: " + str(contar_navios(oculto_jogador)))

    if contar_navios(oculto_jogador) == 0:
        print("\nO computador afundou todos os seus navios. Voce perdeu!")
        print("Jogo feito por: Vinicius, Victor Hugo, Joao Victor")
        print("Obrigado por jogar!")
        break
