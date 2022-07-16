# importando as bibliotecas utilizadas
import pygame
import time
import random

# Define a tamanho da janela
LARGURA = 440
ALTURA = 440
FPS = 30

# Definindo cores básicas para o código
BRANCO = (255, 255, 255)
VERDE = (10, 110, 0,)
AMARELO = (255, 255, 0)


# Iniciando o pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("LABIRINTO")
RELOGIO = pygame.time.Clock()

# Definindo as variáveis do labirinto
grid = []
visitados = []
pilha = []
solucao = {}

# Definindo os eixos e a largura do bloco
a = 400                  # cordenada de saída x
b = 400                  # cordanada de saída y
x = 20                   # eixo x
y = 20                   # eixo y
w = 20                   # largura do bloco

# Contruindo o grid
def construindo_grid(x, y, w):
    for i in range(1,21):
        x = 20                                                            # Define a cordenada inicial de x
        y = y + 20                                                        # inicia uma nova fileira
        for j in range(1, 21):
            pygame.draw.line(tela, BRANCO, [x, y], [x + w, y])              # lado superior do bloco
            pygame.draw.line(tela, BRANCO, [x + w, y], [x + w, y + w])      # lado direito do bloco
            pygame.draw.line(tela, BRANCO, [x + w, y + w], [x, y + w])      # lado inferior do bloco
            pygame.draw.line(tela, BRANCO, [x, y + w], [x, y])              # lado esquerdo do bloco
            grid.append((x, y))                                             # adiciona o bloco para lista grid
            x = x + 20                                                      # move o bloco para uma nova posição

def push_up(x, y):
    pygame.draw.rect(tela, VERDE, (x + 1, y - w + 1, 19, 39), 0)          # desenha um retângulo duas vezes o tamanho do bloco -1
    pygame.display.update()                                               # atualiza as paredes removidas


def push_down(x, y):
    pygame.draw.rect(tela, VERDE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(tela, VERDE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(tela, VERDE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def bloco_unico(x, y):
    pygame.draw.rect(tela, AMARELO, (x + 1, y + 1, 18, 18), 0)          # desenha uma vez a largura do bloco -2
    pygame.display.update()


def backtracking_bloco(x, y):
    pygame.draw.rect(tela, VERDE, (x + 1, y + 1, 18, 18), 0)       # repinta o labirindo de verde
    pygame.display.update()                                        # atualiza os blocos


def bloco_solucao(x, y):
    pygame.draw.rect(tela, AMARELO, (x+8, y+8, 5, 5), 0)           # mostra os blocos da solução na tela
    pygame.display.update()                                        # atualiza os blocos visitados


def constroi_o_labirinto(x, y):
    bloco_unico(x, y)                                              # posição inicial do labirinto
    pilha.append((x, y))                                           # coloca o primeiro bloco na pilha
    visitados.append((x, y))                                       # adiciona o primeiro bloco na lista visitados
    while len(pilha) > 0:                                          # loop até a pilha ficar vazia
        time.sleep(0.01)
        blocos = []                                                # define uma lista de blocos
        if (x + w, y) not in visitados and (x + w, y) in grid:     # lado direito do bloco está disponível?
            blocos.append("direito")                               # se sim, adiciona-o a lista

        if (x - w, y) not in visitados and (x - w, y) in grid:
            blocos.append("esquerdo")

        if (x, y + w) not in visitados and (x, y + w) in grid:
            blocos.append("inferior")

        if (x, y - w) not in visitados and (x, y - w) in grid:
            blocos.append("superior")

        if len(blocos) > 0:                                          # verifica se a lista blocos está vazia
            bloco_escolhido = (random.choice(blocos))                # seleciona um bloco da lista blocos randomicamente

            if bloco_escolhido == "direito":                         # se o bloco específico foi escolhido
                push_right(x, y)                                     # chama a função push_right
                solucao[(x + w, y)] = x, y
                x = x + w                                            # faz este bloco o atual
                visitados.append((x, y))                             # adiciona a lista visitados
                pilha.append((x, y))                                 # coloca o atual bloco na lista pilha

            elif bloco_escolhido == "esquerdo":
                push_left(x, y)
                solucao[(x - w, y)] = x, y
                x = x - w
                visitados.append((x, y))
                pilha.append((x, y))

            elif bloco_escolhido == "inferior":
                push_down(x, y)
                solucao[(x, y + w)] = x, y
                y = y + w
                visitados.append((x, y))
                pilha.append((x, y))

            elif bloco_escolhido == "superior":
                push_up(x, y)
                solucao[(x, y - w)] = x, y
                y = y - w
                visitados.append((x, y))
                pilha.append((x, y))
        else:
            x, y = pilha.pop()                                    # Se não houver blocos disponíveis, retira um bloco na pilha
            bloco_unico(x, y)                                     # usa a função bloco único para mostrar o caminho de volta
            time.sleep(0.1)
            backtracking_bloco(x, y)


def plot_rota_solucao(a, b, x, y):
    bloco_solucao(a, b)                                          # desnha os blocos da solução
    while (a, b) != (x, y):                                      # loop até posição do bloco ser igual a posição inicial
        a, b = solucao[a, b]
        bloco_solucao(a, b)                                      # anima a rota solução
        time.sleep(.01)



construindo_grid(x, 0, w)                 # valor de x, valor de y, largura do bloco
constroi_o_labirinto(x, y)                # chamando a função construtora do labirinto (ponto inicial)
plot_rota_solucao(a, b, x, y)             # chamando a função que mostra o caminho solução ()


###### loop pygame #######
rodar = True
while rodar:
    RELOGIO.tick(FPS)
    # processo de entradas (eventos)
    for event in pygame.event.get():
        # verifica para fechar a janela
        if event.type == pygame.QUIT:
            rodar = False
