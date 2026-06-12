import random

# Tamanho do tabuleiro
LINHAS = 10
COLUNAS = 10

# Cada navio tem um número de identificação (ID), um nome e quantas casas ocupa
NAVIOS = {
    2: ("Porta-aviões", 5),
    3: ("Navio-tanque", 4),
    4: ("Contratorpedeiro", 3),
    5: ("Submarino", 2),
    6: ("Destroier", 1)
}

# Letras que identificam as linhas do tabuleiro na tela
LETRAS_DAS_LINHAS = ['A','B','C','D','E','F','G','H','I','J']


# Cria um tabuleiro 10x10 todo preenchido com '.' (água vazia)
def criar_tabuleiro():
    tabuleiro = []
    for numero_linha in range(LINHAS):
        linha = []
        for numero_coluna in range(COLUNAS):
            linha.append('.')
        tabuleiro.append(linha)
    return tabuleiro


# Imprime o tabuleiro no terminal com os símbolos certos em cada casa
# mostrar_navios=True  → mostra os navios (usado pro próprio jogador ver onde posicionou)
# mostrar_navios=False → esconde os navios (usado pra ver o tabuleiro do computador)
def mostrar_tabuleiro(tabuleiro, nome_do_dono, mostrar_navios=False):
    print("\nTabuleiro do " + nome_do_dono)
    print("    " + "".join(f"{numero_coluna:<5}" for numero_coluna in range(COLUNAS)))

    for indice_linha in range(LINHAS):
        texto_da_linha = f" {LETRAS_DAS_LINHAS[indice_linha]}  "

        for indice_coluna in range(COLUNAS):
            conteudo_da_celula = tabuleiro[indice_linha][indice_coluna]

            # Escolhe o símbolo certo pra cada tipo de celula
            if isinstance(conteudo_da_celula, int) and mostrar_navios:
                simbolo = "🚢"  # célula com navio (só aparece pro dono do tabuleiro)
            elif conteudo_da_celula == '💥':
                simbolo = "💥"  # tiro que acertou um navio
            elif conteudo_da_celula == '❌':
                simbolo = "❌"  # tiro que caiu na água
            else:
                simbolo = "🌊"  # água que ainda não foi atacada

            texto_da_linha += f"{simbolo:<2}  "

        print(texto_da_linha)


# Conta quantos navios ainda estão vivos 
def contar_embarcacoes(info_dos_navios):
    navios_vivos = 0
    for dados_do_navio in info_dos_navios.values():
        if dados_do_navio["células"]:  # lista não vazia = navio ainda vivo
            navios_vivos += 1
    return navios_vivos


# Posiciona todos os navios no tabuleiro
# Se for jogador=True, pede as posições pelo teclado
# Se for jogador=False, o computador sorteia as posições
def posicionar(tabuleiro, info_dos_navios, jogador=True):

    for id_do_navio, (nome_do_navio, tamanho_do_navio) in NAVIOS.items():
        navio_posicionado = False

        # Fica tentando até conseguir posicionar o navio sem conflito
        while not navio_posicionado:

            if jogador:
                print(f"\nVocê está posicionando: {nome_do_navio} (tamanho {tamanho_do_navio})")
                mostrar_tabuleiro(tabuleiro, "Jogador", mostrar_navios=True)

                letra_da_linha = input("Linha inicial (A-J): ").upper()
                if letra_da_linha not in LETRAS_DAS_LINHAS:
                    continue

                try:
                    coluna_inicial = int(input("Coluna inicial (0-9): "))
                except ValueError:
                    continue

                direcao = input("Direcao (H/V): ").upper()
                linha_inicial = LETRAS_DAS_LINHAS.index(letra_da_linha)

            else:
                linha_inicial  = random.randint(0, 9)
                coluna_inicial = random.randint(0, 9)
                direcao        = random.choice(['H', 'V'])

            # Verifica se o navio cabe sem sair do tabuleiro e sem sobrepor outro
            navio_cabe = True
            celulas_do_navio = []

            for passo in range(tamanho_do_navio):

                if direcao == 'H':
                    coluna_atual = coluna_inicial + passo
                    if coluna_atual > 9 or tabuleiro[linha_inicial][coluna_atual] != '.':
                        navio_cabe = False
                        break
                    celulas_do_navio.append((linha_inicial, coluna_atual))

                else:
                    linha_atual = linha_inicial + passo
                    if linha_atual > 9 or tabuleiro[linha_atual][coluna_inicial] != '.':
                        navio_cabe = False
                        break
                    celulas_do_navio.append((linha_atual, coluna_inicial))

            if navio_cabe:
                # Marca o ID do navio em cada célula que ele ocupa
                for (lin, col) in celulas_do_navio:
                    tabuleiro[lin][col] = id_do_navio

                # Salva nome e posições do navio pra consultar durante o jogo
                info_dos_navios[id_do_navio] = {
                    "nome": nome_do_navio,
                    "células": celulas_do_navio
                }

                navio_posicionado = True


# Executa um ataque no tabuleiro do adversário
# Retorna True se acertou um navio (quem acertou joga de novo)
# Retorna False se errou (passa a vez pro outro)
def atacar(tabuleiro_do_alvo, tabuleiro_visivel, info_dos_navios, jogador=True):

    while True:

        if jogador:
            letra_da_linha = input("\nQual linha quer atacar? (A-J): ").upper()
            if letra_da_linha not in LETRAS_DAS_LINHAS:
                continue

            try:
                coluna_atacada = int(input("Qual coluna quer atacar? (0-9): "))
            except ValueError:
                continue

            if coluna_atacada < 0 or coluna_atacada > 9:
                continue

            linha_atacada = LETRAS_DAS_LINHAS.index(letra_da_linha)

        else:
            linha_atacada  = random.randint(0, 9)
            coluna_atacada = random.randint(0, 9)
            print("Computador atacou:", LETRAS_DAS_LINHAS[linha_atacada] + str(coluna_atacada))

        # Não deixa atacar uma posição que já foi atacada antes
        if tabuleiro_visivel[linha_atacada][coluna_atacada] in ['💥', '❌']:
            if jogador:
                print("Você já atacou esse lugar! Escolha outro.")
                continue
            else:
                return False  # computador sorteou posição repetida, vai tentar de novo

        break  # posição válida, sai do loop de escolha

    conteudo_da_celula = tabuleiro_do_alvo[linha_atacada][coluna_atacada]

    if isinstance(conteudo_da_celula, int):  # acertou um navio
        # Marca a célula como atingida nos dois tabuleiros
        tabuleiro_do_alvo[linha_atacada][coluna_atacada] = 0
        tabuleiro_visivel[linha_atacada][coluna_atacada] = '💥'

        # Retira essa célula da lista de células vivas do navio
        navio_atingido = info_dos_navios[conteudo_da_celula]
        navio_atingido["células"].remove((linha_atacada, coluna_atacada))

        print("🎯 Acertou!")

        # Se todas as células do navio foram atingidas, ele afundou
        if not navio_atingido["células"]:
            print(f"🔥 {navio_atingido['nome']} foi afundado!")

        return True  # acertou → joga de novo

    else:
        tabuleiro_visivel[linha_atacada][coluna_atacada] = '❌'
        print("🌊 Errou!")
        return False  # errou → passa a vez


# ==============================
# INÍCIO DO JOGO
# ==============================

print("----------------------------------")
print("Bem vindo ao Batalha Naval!")
print("----------------------------------")

# Tabuleiro real do computador (o jogador nunca vê esse)
tabuleiro_oculto_computador = criar_tabuleiro()

# Tabuleiro real do jogador (onde os navios dele estão)
tabuleiro_oculto_jogador = criar_tabuleiro()

# O que o jogador vê do tabuleiro do computador (começa vazio, vai preenchendo com 💥 e ❌)
tabuleiro_visivel_computador = criar_tabuleiro()

# Guardam as informações dos navios de cada lado
info_navios_computador = {}
info_navios_jogador = {}

try:
    # Posiciona os navios antes de começar — computador primeiro (aleatório), depois o jogador
    posicionar(tabuleiro_oculto_computador, info_navios_computador, jogador=False)
    posicionar(tabuleiro_oculto_jogador, info_navios_jogador, jogador=True)

    # Mostra os dois tabuleiros no início
    mostrar_tabuleiro(tabuleiro_visivel_computador, "Computador")
    mostrar_tabuleiro(tabuleiro_oculto_jogador, "Jogador", mostrar_navios=True)

    # Loop principal — roda até alguém vencer ou o jogador apertar Ctrl+C
    while True:

        # ==============================
        # TURNO DO JOGADOR
        # ==============================
        print("\n--- Sua vez ---")

        # Enquanto o jogador acertar, ele continua atacando
        while atacar(tabuleiro_oculto_computador, tabuleiro_visivel_computador, info_navios_computador, jogador=True):

            mostrar_tabuleiro(tabuleiro_visivel_computador, "Computador")
            print("Embarcações restantes (Computador):", contar_embarcacoes(info_navios_computador))
            print("Embarcações restantes (Você):", contar_embarcacoes(info_navios_jogador))

            # Verifica se o jogador afundou todos os navios do computador
            if contar_embarcacoes(info_navios_computador) == 0:
                print("\n🎉 Parabéns! Você venceu!")
                print("\nJogo desenvolvido por:")
                print("João Vitor Chaves Venancio")
                print("Victor Hugo dos Santos de Camargo")
                print("Vinicius Roxadelli de Almeida")
                raise SystemExit

        mostrar_tabuleiro(tabuleiro_visivel_computador, "Computador")
        mostrar_tabuleiro(tabuleiro_oculto_jogador, "Jogador", mostrar_navios=True)
        print("Embarcações restantes (Computador):", contar_embarcacoes(info_navios_computador))
        print("Embarcações restantes (Você):", contar_embarcacoes(info_navios_jogador))

        # ==============================
        # TURNO DO COMPUTADOR
        # ==============================
        print("\n--- Vez do computador ---")

        # Enquanto o computador acertar, ele continua atacando
        while atacar(tabuleiro_oculto_jogador, tabuleiro_oculto_jogador, info_navios_jogador, jogador=False):

            mostrar_tabuleiro(tabuleiro_oculto_jogador, "Jogador", mostrar_navios=True)
            print("Embarcações restantes (Computador):", contar_embarcacoes(info_navios_computador))
            print("Embarcações restantes (Você):", contar_embarcacoes(info_navios_jogador))

            # Verifica se o computador afundou todos os navios do jogador
            if contar_embarcacoes(info_navios_jogador) == 0:
                print("\n💀 O computador venceu!")
                print("\nJogo desenvolvido por:")
                print("João Vitor Chaves Venancio")
                print("Victor Hugo dos Santos de Camargo")
                print("Vinicius Roxadelli de Almeida")
                print("\nObrigado por jogar nosso jogo, volte sempre!")
                raise SystemExit

        mostrar_tabuleiro(tabuleiro_visivel_computador, "Computador")
        mostrar_tabuleiro(tabuleiro_oculto_jogador, "Jogador", mostrar_navios=True)
        print("Embarcações restantes (Computador):", contar_embarcacoes(info_navios_computador))
        print("Embarcações restantes (Você):", contar_embarcacoes(info_navios_jogador))

# Se o jogador apertar Ctrl+C em qualquer momento, encerra sem travar
except KeyboardInterrupt:
    print("\n\n⛔ Jogo interrompido pelo usuário. Até a próxima!")
    print("\nJogo desenvolvido por:")
    print("João Vitor Chaves Venancio")
    print("Victor Hugo dos Santos de Camargo")
    print("Vinicius Roxadelli de Almeida")
