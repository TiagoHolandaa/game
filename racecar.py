# Importa as bibliotecas necessárias
import pygame
import time
import math
from utils import scale_image, blit_rotate_center

# Constantes
GRAMA = scale_image(pygame.image.load("img/grass.jpg"), 2.5)
PISTA = scale_image(pygame.image.load("img/track.png"), 0.9)

BORDA_PISTA = scale_image(pygame.image.load("img/track-border.png"), 0.9)
MASCARA_BORDA_PISTA = pygame.mask.from_surface(BORDA_PISTA)

CHEGADA = scale_image(pygame.image.load("img/finish.png"), 0.78)
MASCARA_CHEGADA = pygame.mask.from_surface(CHEGADA)
POSICAO_CHEGADA = (85, 250)

CARRO = scale_image(pygame.image.load("img/carro.png"), 0.05)
# Inicializa o Pygame
LARGURA, ALTURA = PISTA.get_width(), PISTA.get_height()
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Corrida!")
pygame.font.init()
# Variáveis globais
tempo_inicial = time.time()
tempo_jogo = 0
# Define a taxa de quadros
FPS = 60


class CarroAbstrato:
    def __init__(self, max_vel, velocidade_rotacao):
        # Atributos do carro
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.velocidade_rotacao = velocidade_rotacao
        self.angulo = 0
        self.x, self.y = self.POSICAO_INICIAL
        self.aceleracao = 0.05
    # Métodos
    def girar(self, esquerda=False, direita=False):
        # Gira o carro para a esquerda ou para a direita
        if esquerda:
            self.angulo += self.velocidade_rotacao
        elif direita:
            self.angulo -= self.velocidade_rotacao

    def desenhar(self, janela):
        # Desenha o carro na tela
        blit_rotate_center(janela, self.img, (self.x, self.y), self.angulo)

    def mover_frente(self):
        # Move o carro para frente
        self.vel = min(self.vel + self.aceleracao, self.max_vel)
        self.mover()

    def mover_tras(self):
        # Move o carro para trás
        self.vel = max(self.vel - self.aceleracao, -self.max_vel/2)
        self.mover()

    def mover(self):
        # Move o carro de acordo com sua velocidade e ângulo
        radianos = math.radians(self.angulo)
        vertical = math.cos(radianos) * self.vel
        horizontal = math.sin(radianos) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def colidir(self, mascara, x=0, y=0):
        # Verifica se o carro colidiu com algo
        mascara_carro = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        # Verifica se há colisão com a máscara da borda da pista 
        ponto_de_interesse = mascara.overlap(mascara_carro, offset)
        return ponto_de_interesse

    def resetar(self):
        # Reseta a posição e a velocidade do carro
        self.x, self.y = self.POSICAO_INICIAL
        self.angulo = 0
        self.vel = 0


class CarroJogador(CarroAbstrato):
    IMG = CARRO
    POSICAO_INICIAL = (110, 200)

    def reduzir_velocidade(self):
        # Reduz a velocidade do carro
        self.vel = max(self.vel - self.aceleracao / 2, 0)
        self.mover()

    def quicar(self):
        self.vel = -self.vel
        self.mover()


# Função para desenhar os elementos na tela
def desenhar(janela, imagens, carro_jogador):
    # Desenha as imagens de fundo
    for img, pos in imagens:
        janela.blit(img, pos)

    # Desenha o carro do jogador
    carro_jogador.desenhar(janela)
    # Desenha o tempo de jogo
    fonte = pygame.font.SysFont(None, 36)
    texto_tempo = fonte.render(f"Tempo: {tempo_jogo}", True, (255, 255, 255))
    JANELA.blit(texto_tempo, (10, 10))
    # Atualiza a tela
    pygame.display.update()

# Função para mover o carro do jogador
def mover_jogador(carro_jogador):
    # Obtém as teclas pressionadas
    teclas = pygame.key.get_pressed()
    movido = False

    # Gira o carro para a esquerda ou para a direita
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        carro_jogador.girar(esquerda=True)
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        carro_jogador.girar(direita=True)
    # Acelera o carro
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        movido = True
        carro_jogador.mover_frente()
    # Frena o carro
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        movido = True
        carro_jogador.mover_tras()
    # Reduz a velocidade do carro se ele não estiver sendo movido
    if not movido:
        carro_jogador.reduzir_velocidade()

def tela_inicial():
    tela_aberta = True
    botao_play = pygame.Rect(250, 300, 100, 50)  # Coordenadas do botão play

    while tela_aberta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_play.collidepoint(evento.pos):
                    return

        JANELA.fill((0, 0, 0))
        imagem_fundo = scale_image(pygame.image.load("img/home.png"), 1.8)
        JANELA.blit(imagem_fundo, (0, 0))

        # Desenha o botão "play" no centro da tela
        pygame.draw.rect(JANELA, (0, 128, 255), botao_play)
        fonte = pygame.font.SysFont(None, 36)
        texto_play = fonte.render("PLAY", True, (255, 255, 255))
        JANELA.blit(texto_play, (botao_play.centerx - texto_play.get_width() // 2, botao_play.centery - texto_play.get_height() // 2))

        # Desenha o título do jogo
        fonte_titulo = pygame.font.SysFont(None, 60)
        texto_titulo = fonte_titulo.render("Nosso Jogo de Corrida", True, (255, 255, 255))
        JANELA.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 100))

        pygame.display.update()

# Chama a tela inicial antes do loop principal
tela_inicial()

executando = True
relogio = pygame.time.Clock()
imagens = [(GRAMA, (0, 0)), (PISTA, (0, 0)),
           (CHEGADA, POSICAO_CHEGADA), (BORDA_PISTA, (0, 0))]
carro_jogador = CarroJogador(2, 2)
# Inicia o loop principal
while executando:
    relogio.tick(FPS)

    # Verifica se o botão foi clicado
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
    # Desenha os elementos na tela
    desenhar(JANELA, imagens, carro_jogador)
    # Atualiza o tempo
    tempo_decorrido = time.time() - tempo_inicial
    tempo_jogo = int(tempo_decorrido)
    # Verifica os eventos
    for evento in pygame.event.get():
        # Fecha o jogo se o usuário clicar no botão "X"
        if evento.type == pygame.QUIT:
            executando = False
            break
    # Move o carro do jogador
    mover_jogador(carro_jogador)
    # Verifica se o carro colidiu com a borda da pista
    if carro_jogador.colidir(MASCARA_BORDA_PISTA) != None:
        carro_jogador.quicar()
    # Verifica se o carro chegou à linha de chegada
    colisao_ponto_chegada = carro_jogador.colidir(MASCARA_CHEGADA, *POSICAO_CHEGADA)
    if colisao_ponto_chegada != None:
        if colisao_ponto_chegada[1] == 0:
            carro_jogador.quicar()
        else:
            carro_jogador.resetar()
            print("chegada")
            
# Fecha o Pygame
pygame.quit()
