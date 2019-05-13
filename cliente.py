import sys
import Pyro4
import Pyro4.util
from random import choice
import  time


sys.excepthook = Pyro4.util.excepthook


def IA_vez(server, comp_escolha, humano_escolha):
    profundidade = len(server.celulas_vazias())
    if profundidade == 0 or server.fim_jogo():
        return

    server.limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    print(server.exibe_tabuleiro(comp_escolha, humano_escolha))

    if profundidade == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = server.minimax(profundidade, server.comp())
        x, y = move[0], move[1]

    server.exec_movimento(x, y, server.comp())
    time.sleep(1)


def HUMANO_vez(server, comp_escolha, humano_escolha):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(server.celulas_vazias())
    if profundidade == 0 or server.fim_jogo():
        return

    # Dicionário de movimentos válidos
    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    server.limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    print(server.exibe_tabuleiro(comp_escolha, humano_escolha))

    while movimento < 1 or movimento > 9:
        try:
            movimento = int(input('Use numero (1..9): '))
            coord = movimentos[movimento]
            tenta_movimento = server.exec_movimento(coord[0], coord[1], server.hum())

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')


def main():
    # self.nome = nome
    server = Pyro4.Proxy("PYRONAME:teste.jogo")

    server.limpa_console()
    humano_escolha = ''  # Pode ser X ou O
    comp_escolha = ''  # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro

    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    server.limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Laço principal do jogo
    while len(server.celulas_vazias()) > 0 and not server.fim_jogo():
        if primeiro == 'N':
            IA_vez(server, comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(server, comp_escolha, humano_escolha)
        IA_vez(server, comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if server.vitoria(server.hum()):
        server.limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        print(server.exibe_tabuleiro(comp_escolha, humano_escolha))
        print('Você Venceu!')
    elif server.vitoria(server.comp()):
        server.limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        print(server.exibe_tabuleiro(comp_escolha, humano_escolha))
        print('Você Perdeu!')
    else:
        server.limpa_console()
        print(server.exibe_tabuleiro(comp_escolha, humano_escolha))
        print('Empate!')

    exit()


if __name__ == '__main__':

    main()