import random

# tabuleiro 10x10
LINHAS = 10
COLUNAS = 10

# cria matriz vazia com zeros
def criar_tabuleiro():
    tabuleiro = []
    for i in range(LINHAS):
        linha = []
        for j in range(COLUNAS):
            linha.append('.')
        tabuleiro.append(linha)
    return tabuleiro

# mostra o tabuleiro na tela
def mostrar_tabuleiro(tabuleiro, nome):
    letras = ['A','B','C','D','E','F','G','H','I','J']
    print("\nTabuleiro do " + nome)
    print("    0  1  2  3  4  5  6  7  8  9")
    for i in range(LINHAS):
        linha_str = " " + letras[i] + "  "
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

# jogador escolhe onde colocar os navios
def posicionar_jogador(tabuleiro):
    letras = ['A','B','C','D','E','F','G','H','I','J']
    navios = [("Porta-avioes", 5), ("Navio-tanque", 4), ("Contratorpedeiro", 3), ("Submarino", 2), ("Destroier", 1)]
    print("\nPosicione seus navios no tabuleiro")
    print("Linhas: A ate J  |  Colunas: 0 ate 9  |  Direcao: H ou V")

    for navio, tamanho in navios:
        posicionado = False
        while posicionado == False:
            print("\n" + navio + " (tamanho " + str(tamanho) + ")")
            mostrar_tabuleiro(tabuleiro, "Jogador")
            letra = input("Linha inicial (A-J): ").upper()
            coluna = int(input("Coluna inicial (0-9): "))
            direcao = input("Direcao (H/V): ").upper()

            # converte letra pra indice
            linha = -1
            for i in range(len(letras)):
                if letras[i] == letra:
                    linha = i

            if linha == -1:
                print("Linha invalida!")
            elif coluna < 0 or coluna > 9:
                print("Coluna invalida!")
            elif direcao != 'H' and direcao != 'V':
                print("Direcao invalida! Use H ou V")
            else:
                # verifica se o navio cabe e nao tem colisao
                cabe = True
                for k in range(tamanho):
                    if direcao == 'H':
                        if coluna + k > 9:
                            cabe = False
                        elif tabuleiro[linha][coluna + k] != '.':
                            cabe = False
                    else:
                        if linha + k > 9:
                            cabe = False
                        elif tabuleiro[linha + k][coluna] != '.':
                            cabe = False

                if cabe == False:
                    print("Nao cabe ai! Tente outra posicao.")
                else:
                    # coloca o navio
                    for k in range(tamanho):
                        if direcao == 'H':
                            tabuleiro[linha][coluna + k] = 1
                        else:
                            tabuleiro[linha + k][coluna] = 1
                    posicionado = True

# computador coloca os navios de forma aleatoria
def posicionar_computador(tabuleiro):
    navios = [("Porta-avioes", 5), ("Navio-tanque", 4), ("Contratorpedeiro", 3), ("Submarino", 2), ("Destroier", 1)]

    for navio, tamanho in navios:
        posicionado = False
        while posicionado == False:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
            direcao = random.choice(['H', 'V'])

            cabe = True
            for k in range(tamanho):
                if direcao == 'H':
                    if coluna + k > 9:
                        cabe = False
                    elif tabuleiro[linha][coluna + k] != '.':
                        cabe = False
                else:
                    if linha + k > 9:
                        cabe = False
                    elif tabuleiro[linha + k][coluna] != '.':
                        cabe = False

            if cabe == True:
                for k in range(tamanho):
                    if direcao == 'H':
                        tabuleiro[linha][coluna + k] = 1
                    else:
                        tabuleiro[linha + k][coluna] = 1
                posicionado = True

# jogador ataca
def atacar_jogador(oculto_computador, visivel_computador):
    letras = ['A','B','C','D','E','F','G','H','I','J']

    letra = input("\nQual linha quer atacar? (A-J): ").upper()
    coluna = int(input("Qual coluna quer atacar? (0-9): "))

    linha = -1
    for i in range(len(letras)):
        if letras[i] == letra:
            linha = i

    if linha == -1 or coluna < 0 or coluna > 9:
        print("Coordenada invalida!")
        return

    if visivel_computador[linha][coluna] == 'X' or visivel_computador[linha][coluna] == 'O':
        print("Voce ja atacou esse lugar!")
        return

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
    letras = ['A','B','C','D','E','F','G','H','I','J']

    while True:
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        if [linha, coluna] not in ja_atacados:
            ja_atacados.append([linha, coluna])
            break

    print("Computador atacou: " + letras[linha] + str(coluna))

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
oculto_computador = criar_tabuleiro()
oculto_jogador = criar_tabuleiro()
visivel_computador = criar_tabuleiro()
visivel_jogador = criar_tabuleiro()

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
        print("Jogo feito por: Vinicius e [colega]")
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
        print("Jogo feito por: Vinicius, Victor Hugo, João Victor")
        print("Obrigado por jogar!")
        break
