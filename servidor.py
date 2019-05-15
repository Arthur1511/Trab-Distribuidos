# !/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system
import Pyro4

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""


# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa vazio, com zero em todas posições.


@Pyro4.expose
@Pyro4.behavior(instance_mode="session")
class Jogo(object):

    objects = []

    def __init__(self):
        # self.nome = None
        self.HUMANO = -1
        self.COMP = +1
        self.estado = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]

    def __repr__(self):
        return '<{} - {}>\n'.format(self.nome, self.estado)

    def save(self):
        self.__class__.objects.append(self)

    @classmethod
    def buscar(cls, nome):

        for x, jogo in enumerate(cls.objects):

            if jogo.nome == nome:
                return x

    @classmethod
    def all(cls):
        return cls.objects

    def comp(self):
        return self.COMP

    def hum(self):
        return self.HUMANO

    """
    Funcao para avaliacao heuristica do estado.
    :parametro (estado): o estado atual do tabuleiro
    :returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
     """

    def avaliacao(self):
        if self.vitoria(self.COMP):
            placar = +1
        elif self.vitoria(self.HUMANO):
            placar = -1
        else:
            placar = 0

        return placar

    """ fim avaliacao (estado)------------------------------------- """

    def vitoria(self, jogador):
        """
        Esta funcao testa se um jogador especifico vence. Possibilidades:
        * Tres linhas     [X X X] or [O O O]
        * Tres colunas    [X X X] or [O O O]
        * Duas diagonais  [X X X] or [O O O]
        :param. (estado): o estado atual do tabuleiro
        :param. (jogador): um HUMANO ou um Computador
        :return: True se jogador vence
        """
        win_estado = [
            [self.estado[0][0], self.estado[0][1], self.estado[0][2]],  # toda linha 1
            [self.estado[1][0], self.estado[1][1], self.estado[1][2]],  # toda linha 2
            [self.estado[2][0], self.estado[2][1], self.estado[2][2]],  # toda linha 3
            [self.estado[0][0], self.estado[1][0], self.estado[2][0]],  # toda coluna 1
            [self.estado[0][1], self.estado[1][1], self.estado[2][1]],  # toda coluna 2
            [self.estado[0][2], self.estado[1][2], self.estado[2][2]],  # toda coluna 3
            [self.estado[0][0], self.estado[1][1], self.estado[2][2]],  # diagonal principal
            [self.estado[2][0], self.estado[1][1], self.estado[0][2]],  # diagonal secundária
        ]
        # Se um, dentre todos os alinhamentos pertence um mesmo jogador,
        # então o jogador vence!
        if [jogador, jogador, jogador] in win_estado:
            return True
        else:
            return False

    """ ---------------------------------------------------------- """

    """
    Testa fim de jogo para ambos jogadores de acordo com estado atual
    return: será fim de jogo caso ocorra vitória de um dos jogadores.
    """

    def fim_jogo(self):
        return self.vitoria(self.HUMANO) or self.vitoria(self.COMP)

    """ ---------------------------------------------------------- """

    """
    Verifica celular vazias e insere na lista para informar posições
    ainda permitidas para próximas jogadas.
    """

    def celulas_vazias(self):
        celulas = []
        for x, row in enumerate(self.estado):
            for y, cell in enumerate(row):
                if cell == 0:
                    celulas.append([x, y])
        return celulas

    """ ---------------------------------------------------------- """

    """
    Um movimento é valido se a célula escolhida está vazia.
    :param (x): coordenada X
    :param (y): coordenada Y
    :return: True se o tabuleiro[x][y] está vazio
    """

    def movimento_valido(self, x, y):
        if [x, y] in self.celulas_vazias():
            return True
        else:
            return False

    """ ---------------------------------------------------------- """

    """
    Executa o movimento no tabuleiro se as coordenadas são válidas
    :param (x): coordenadas X
    :param (y): coordenadas Y
    :param (jogador): o jogador da vez
    """

    def exec_movimento(self, x, y, jogador):
        if self.movimento_valido(int(x), int(y)):
            self.estado[x][y] = jogador
            return True
        else:
            return False

    """ ---------------------------------------------------------- """

    """
    Função da IA que escolhe o melhor movimento
    :param (estado): estado atual do tabuleiro
    :param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
    mas nunca será nove neste caso (veja a função iavez())
    :param (jogador): um HUMANO ou um Computador
    :return: uma lista com [melhor linha, melhor coluna, melhor placar]
    """

    def minimax(self, profundidade, jogador):
        int(profundidade)
        int(jogador)
        # valor-minmax(estado)
        if jogador == self.COMP:
            melhor = [-1, -1, -infinity]
        else:
            melhor = [-1, -1, +infinity]

        # valor-minimax(estado) = avaliacao(estado)
        if profundidade == 0 or self.fim_jogo():
            placar = self.avaliacao()
            return [-1, -1, placar]

        for cell in self.celulas_vazias():
            x, y = cell[0], cell[1]
            self.estado[x][y] = jogador
            placar = self.minimax(profundidade - 1, -jogador)
            self.estado[x][y] = 0
            placar[0], placar[1] = x, y

            if jogador == self.COMP:
                if placar[2] > melhor[2]:
                    melhor = placar  # valor MAX
            else:
                if placar[2] < melhor[2]:
                    melhor = placar  # valor MIN
        return melhor

    """ ---------------------------------------------------------- """

    """
    Limpa o console para SO Windows
    """

    def limpa_console(self):
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

    """ ---------------------------------------------------------- """

    """
    Imprime o tabuleiro no console
    :param. (estado): estado atual do tabuleiro
    """

    def exibe_tabuleiro(self, comp_escolha, humano_escolha):
        # str(comp_escolha)
        # str(humano_escolha)
        exibir = '----------------\n'
        for row in self.estado:
            exibir += '\n----------------\n'
            for cell in row:
                if cell == +1:
                   exibir += '|' + ' ' + comp_escolha + ' ' + '|'
                elif cell == -1:
                    exibir += '|' + ' ' + humano_escolha + ' ' + '|'
                else:
                   exibir += '|' + ' ' + ' ' + ' ' + '|'
        exibir += '\n----------------\n'

        return exibir

    """ ---------------------------------------------------------- """

Pyro4.Daemon.serveSimple({Jogo: "teste.jogo"}, ns=True)


