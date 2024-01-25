##### IFMA Velozes e Estudiosos #####
#Versão 0.2.0
import pygame
import random


pygame.init()

#tela 800x600
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('IFMA Velozes e Estudiosos')

#carregar background
bg = pygame.image.load('Corrida/bg.jpg').convert()
bg_overlap = pygame.image.load('Corrida/bg.jpg').convert()
bg_pos = 0
bg_overlap_pos = -altura_tela
bg_speed = 5
mover_bg = True

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# Configurações do carro
carro_largura = 60
carro = pygame.image.load('Corrida/car.png')  
carro = pygame.transform.scale(carro, (carro_largura, 110))
# hit_box_carro = pygame.Rect(0, 0, carro_largura, 110)

# Posição inicial do carro
x = (largura_tela * 0.45)
y = (altura_tela * 0.8)

# Configurações dos obstáculos
def generate_obstacle():
    return random.randrange(0, largura_tela)
obstaculo_largura = 50
obstaculo_altura = 100
obstaculo_cor = (255, 0, 0)  
obstaculo_velocidade = 7 
obstaculo_x = generate_obstacle()
obstaculo_y = -600

# Desenhando os obstáculos
def desenha_obstaculo(x, y, largura, altura, cor):
    pygame.draw.rect(tela, cor, [x, y, largura, altura])

# Redesenhando a tela
def redesenhar_tela():
    #backgorund scroll
    global bg_pos, bg_overlap_pos, bg_speed, mover_bg
    if mover_bg:
        if bg_pos >= altura_tela:
            bg_pos = -altura_tela
        if bg_overlap_pos >= altura_tela:
            bg_overlap_pos = -altura_tela

        bg_pos += bg_speed
        bg_overlap_pos += bg_speed
        tela.blit(bg, (0, bg_pos))
        tela.blit(bg_overlap, (0, bg_overlap_pos))
        tela.blit(carro, (x, y))
        desenha_obstaculo(obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura, obstaculo_cor)
        pygame.display.update()

# Parte principal do jogo (aqui executo a criação do loop)
jogo_ativo = True
clock = pygame.time.Clock()

while jogo_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_ativo = False

    obstaculo_x += int((x - obstaculo_x) * 0.04)

    #movimentação do carro
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #se x for maior que 0, ou seja, se estiver dentro da tela, ele pode se mover
        if x>0:
            x -= 5
        else:
            pass
    if keys[pygame.K_RIGHT]:
        #se x for menor que a largura da tela menos a largura do carro, ou seja, se estiver dentro da tela, ele pode se mover
        if x<largura_tela - carro_largura - 1:
            x += 5
        else:
            pass

    #sair do jogo ao apertar esc
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    #reincia o jogo
    if obstaculo_velocidade == 0:
        if keys[pygame.K_SPACE]:
            mover_bg = True
            obstaculo_velocidade = 7
            obstaculo_x = random.randrange(0, largura_tela)
            obstaculo_y = -600
            x = (largura_tela * 0.45)
            y = (altura_tela * 0.8)

    #obstaculo
    obstaculo_y += obstaculo_velocidade
    if obstaculo_y > altura_tela:
        obstaculo_y = 0 - obstaculo_altura
        obstaculo_x = random.randrange(0, largura_tela)

    #vidas
    
    
    #colisão
    if (obstaculo_y + obstaculo_altura) > y:
        if obstaculo_x > x and obstaculo_x < x + carro_largura or obstaculo_x + obstaculo_largura > x and obstaculo_x + obstaculo_largura < x + carro_largura:
            obstaculo_velocidade = 0
            pygame.font.init()
            fonte = pygame.font.get_default_font()
            fonte_gameover = pygame.font.SysFont(fonte, 90)
            text_gameover = fonte_gameover.render('GAME OVER', 1, (255, 0, 0))
            fonte_tryagain = pygame.font.SysFont(fonte, 30)
            text_tryagain = fonte_tryagain.render('ESPACO PARA TENTAR NOVAMENTE', 1, (0, 0, 0))
            tela.blit(text_gameover, (largura_tela/2 - text_gameover.get_width()/2, altura_tela/2 - text_gameover.get_height()/2))
            tela.blit(text_tryagain, (largura_tela/2 - text_tryagain.get_width()/2, altura_tela/2 - text_tryagain.get_height()/2 + 50))
            pygame.display.update()
            mover_bg = False

    redesenhar_tela()
    clock.tick(75)

pygame.quit()
