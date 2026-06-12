import random

# Dimensões do tabuleiro
LINHAS = 10
COLUNAS = 10

# Definição dos navios com IDs únicos e seus tamanhos
NAVIOS = {
    2: ("Porta-aviões", 5),
    3: ("Navio-tanque", 4),
    4: ("Contratorpedeiro", 3),
    5: ("Submarino", 2),
    6: ("Destroier", 1)
}

# Cria um tabuleiro vazio preenchido com '.'
def criar_tabuleiro():
    return [['.' for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Exibe o tabuleiro na tela
def mostrar_tabuleiro(tabuleiro, nome, mostrar_navios=False):
    letras = ['A','B','C','D','E','F','G','H','I','J']

    print("\nTabuleiro do " + nome)
    print("    " + "".join(f"{i:<5}" for i in range(COLUNAS)))

    for i in range(LINHAS):
        linha_str = f" {letras[i]}  "

        for j in range(COLUNAS):
            celula = tabuleiro[i][j]

            # Define qual símbolo será mostrado
            if isinstance(celula, int) and mostrar_navios:
                simbolo = "🚢"
            elif celula == '💥':
                simbolo = "💥"
            elif celula == '❌':
                simbolo = "❌"
            else:
                simbolo = "🌊"

            linha_str += f"{simbolo:<2}  "

        print(linha_str)

# Conta quantas embarcações ainda não foram afundadas
def contar_embarcacoes(navios_info):
    return len([n for n in navios_info.values() if n["células"]])

# Posiciona os navios do jogador ou do computador
def posicionar(tabuleiro, navios_info, jogador=True):
    letras = ['A','B','C','D','E','F','G','H','I','J']

    for navio_id, (nome, tamanho) in NAVIOS.items():
        posicionado = False

        while not posicionado:

            # Posicionamento manual do jogador
            if jogador:
                print(f"\nVocê está posicionando: {nome} (tamanho {tamanho})")
                mostrar_tabuleiro(tabuleiro, "Jogador", mostrar_navios=True)

                letra = input("Linha inicial (A-J): ").upper()

                if letra not in letras:
                    continue

                try:
                    coluna = int(input("Coluna inicial (0-9): "))
                except ValueError:
                    continue

                direcao = input("Direcao (H/V): ").upper()
                linha = letras.index(letra)

            # Posicionamento automático do computador
            else:
                linha = random.randint(0, 9)
                coluna = random.randint(0, 9)
                direcao = random.choice(['H','V'])

            cabe = True
            coords = []

            # Verifica se o navio cabe na posição escolhida
            for k in range(tamanho):

                if direcao == 'H':
                    if coluna + k > 9 or tabuleiro[linha][coluna + k] != '.':
                        cabe = False
                        break

                    coords.append((linha, coluna + k))

                else:
                    if linha + k > 9 or tabuleiro[linha + k][coluna] != '.':
                        cabe = False
                        break

                    coords.append((linha + k, coluna))

            # Posiciona o navio no tabuleiro
            if cabe:
                for (x, y) in coords:
                    tabuleiro[x][y] = navio_id

                navios_info[navio_id] = {
                    "nome": nome,
                    "células": coords
                }

                posicionado = True

# Realiza um ataque no tabuleiro adversário
def atacar(tabuleiro_alvo, tabuleiro_visivel, navios_info, jogador=True):
    letras = ['A','B','C','D','E','F','G','H','I','J']

    while True:

        # Jogada do jogador
        if jogador:
            letra = input("\nQual linha quer atacar? (A-J): ").upper()

            if letra not in letras:
                continue

            try:
                coluna = int(input("Qual coluna quer atacar? (0-9): "))
            except ValueError:
                continue

            if coluna < 0 or coluna > 9:
                continue

            linha = letras.index(letra)

        # Jogada aleatória do computador
        else:
            linha, coluna = random.randint(0, 9), random.randint(0, 9)
            print("Computador atacou:", letras[linha] + str(coluna))

        # Impede ataques repetidos
        if tabuleiro_visivel[linha][coluna] in ['💥','❌']:
            if jogador:
                print("Você já atacou esse lugar! Escolha outro.")
                continue
            else:
                return False

        break

    celula = tabuleiro_alvo[linha][coluna]

    # Verifica se acertou um navio
    if isinstance(celula, int):

        tabuleiro_alvo[linha][coluna] = 0
        tabuleiro_visivel[linha][coluna] = '💥'

        navio = navios_info[celula]
        navio["células"].remove((linha, coluna))

        print("🎯 Acertou!")

        # Verifica se o navio foi afundado
        if not navio["células"]:
            print(f"🔥 {navio['nome']} foi afundado!")

        return True

    # Caso erre o ataque
    else:
        tabuleiro_visivel[linha][coluna] = '❌'
        print("🌊 Errou!")
        return False

# ==============================
# INÍCIO DO JOGO
# ==============================

print("----------------------------------")
print("Bem vindo ao Batalha Naval!")
print("----------------------------------")

# Criação dos tabuleiros
oculto_computador = criar_tabuleiro()
oculto_jogador = criar_tabuleiro()
visivel_computador = criar_tabuleiro()

# Dicionários para armazenar informações dos navios
navios_computador = {}
navios_jogador = {}
try:
    # Posicionamento inicial dos navios
    posicionar(oculto_computador, navios_computador, jogador=False)
    posicionar(oculto_jogador, navios_jogador, jogador=True)

    # Exibe os tabuleiros iniciais
    mostrar_tabuleiro(visivel_computador, "Computador")
    mostrar_tabuleiro(oculto_jogador, "Jogador", mostrar_navios=True)



    # Loop principal do jogo
    while True:

        # ==============================
        # TURNO DO JOGADOR
        # ==============================
        print("\n--- Sua vez ---")

        while atacar(oculto_computador, visivel_computador, navios_computador, jogador=True):

            mostrar_tabuleiro(visivel_computador, "Computador")

            print("Embarcações restantes (Computador):",
                  contar_embarcacoes(navios_computador))

            print("Embarcações restantes (Você):",
                  contar_embarcacoes(navios_jogador))

            # Verifica vitória do jogador
            if contar_embarcacoes(navios_computador) == 0:
                print("\n🎉 Parabéns! Você venceu!")

                print("\nJogo desenvolvido por:")
                print("João Vitor Chaves Venancio")
                print("Victor Hugo dos Santos de Camargo")
                print("Vinicius Roxadelli de Almeida")

                raise SystemExit

        mostrar_tabuleiro(visivel_computador, "Computador")
        mostrar_tabuleiro(oculto_jogador, "Jogador", mostrar_navios=True)

        print("Embarcações restantes (Computador):",
              contar_embarcacoes(navios_computador))

        print("Embarcações restantes (Você):",
              contar_embarcacoes(navios_jogador))

        # ==============================
        # TURNO DO COMPUTADOR
        # ==============================
        print("\n--- Vez do computador ---")

        while atacar(oculto_jogador, oculto_jogador, navios_jogador, jogador=False):

            mostrar_tabuleiro(oculto_jogador, "Jogador", mostrar_navios=True)

            print("Embarcações restantes (Computador):",
                  contar_embarcacoes(navios_computador))

            print("Embarcações restantes (Você):",
                  contar_embarcacoes(navios_jogador))

            # Verifica vitória do computador
            if contar_embarcacoes(navios_jogador) == 0:
                print("\n💀 O computador venceu!")

                print("\nJogo desenvolvido por:")
                print("João Vitor Chaves Venancio")
                print("Victor Hugo dos Santos de Camargo")
                print("Vinicius Roxadelli de Almeida")

                print("\nObrigado por jogar nosso jogo, volte sempre!")

                raise SystemExit

        mostrar_tabuleiro(visivel_computador, "Computador")
        mostrar_tabuleiro(oculto_jogador, "Jogador", mostrar_navios=True)

        print("Embarcações restantes (Computador):",
              contar_embarcacoes(navios_computador))

        print("Embarcações restantes (Você):",
              contar_embarcacoes(navios_jogador))

# Trata encerramento com CTRL+C
except KeyboardInterrupt:
    print("\n\n⛔ Jogo interrompido pelo usuário. Até a próxima!")