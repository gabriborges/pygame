import pygame
import random
# Implementações obrigatórias realizadas:
#1 - Ao colidir exibir um som; **Novo**
#2 - A partir de 10 obstáculos ultrapassados, incrementar a velocidade até o limite 10 (atual 7); **Novo**
#3 - Quando incrementar a velocidade aparecer na tela informando que aumentou de nível (velocidade); **Novo**

# Implementações extras realizadas:
# 4. Repaginação completa do código para orientação a objetos. **Novo**
# 5. Mecânica de vidas: o jogador começa com 3 vidas e perde uma a cada colisão (interface gráfica também). **Novo**
# 6. ‘IA’ dos obstáculos: obstáculos agora seguem o carro.
# 7. Tela de Game Over
# 8. Recomeçar o jogo (com a tecla espaço)
# 9. Fechar o jogo (com a tecla esc)


class Jogo:
    def __init__(self):
        pygame.init()

        # Tela 800x600
        self.largura_tela = 800
        self.altura_tela = 600
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('IFMA Velozes e Estudiosos')

        # Background
        self.bg = pygame.image.load('Corrida/bg.jpg').convert()
        self.bg_overlap = pygame.image.load('Corrida/bg.jpg').convert()
        self.bg_pos = 0
        self.bg_overlap_pos = -self.altura_tela
        self.bg_speed = 4
        self.mover_bg = True
        
        # Cores
        self.preto = (0, 0, 0)
        self.branco = (255, 255, 255)

        # Configurações do carro
        self.carro_largura = 60
        self.carro = pygame.image.load('Corrida/car.png')
        self.carro = pygame.transform.scale(self.carro, (self.carro_largura, 110))
        self.x = (self.largura_tela * 0.45)
        self.y = (self.altura_tela * 0.83)
        self.vidas = 3
        self.invulneravel = False
        self.coracao = pygame.image.load('Corrida/heart.png')

        #efeito de som
        self.batida_sfx = pygame.mixer.Sound('Corrida/crash.mp3')

        # Configurações dos obstáculos
        self.obstaculo_largura = 50
        self.obstaculo_altura = 100
        self.obstaculo_cor = (255, 0, 0)
        self.obstaculo_velocidade_padrao = 7
        self.obstaculo_velocidade = 7
        self.obstaculo_x = self.gerando_obstaculos()
        self.obstaculo_y = -600
        self.obstaculo_contador = 0

        self.popup_velocidade = ""
        self.popup_velocidade_timer = 0

        self.jogo_ativo = True
        self.clock = pygame.time.Clock()

    # Gerando e desenhando obstáculos
    def gerando_obstaculos(self):
        return random.randrange(0, self.largura_tela)
    def desenha_obstaculo(self, x, y, largura, altura, cor):
        pygame.draw.rect(self.tela, cor, [x, y, largura, altura])

    def desenha_popup_velocidade(self, texto):
        pygame.font.init()
        fonte = pygame.font.get_default_font()
        fonte_popup = pygame.font.SysFont(fonte, 30)
        text_popup = fonte_popup.render(texto, 1, (255, 255, 0))
        self.tela.blit(text_popup, (self.largura_tela // 2 - text_popup.get_width() // 2, self.altura_tela // 2 - text_popup.get_height() // 2 - 100))
        pygame.display.update()

    def desenha_velocimetro(self):
        if self.obstaculo_contador - 10 > 0 and self.obstaculo_velocidade < 10:
            self.obstaculo_velocidade += 1
            self.obstaculo_contador = 0
            self.popup_velocidade = f'Velocidade aumentada: {self.obstaculo_velocidade} km/h'
            self.popup_velocidade_timer = pygame.time.get_ticks()
        if self.obstaculo_velocidade <10:
            if self.popup_velocidade_timer > 0 and pygame.time.get_ticks() - self.popup_velocidade_timer < 1500:
                self.desenha_popup_velocidade(self.popup_velocidade)
            else:
                self.popup_velocidade_timer = 0

        pygame.font.init()
        fonte = pygame.font.get_default_font()
        fonte_velocimetro = pygame.font.SysFont(fonte, 40)
        text_velocimetro = fonte_velocimetro .render(f'Speed: {self.obstaculo_velocidade} km/h', 1, (255, 0, 0))
        self.tela.blit(text_velocimetro, (0, 570))

    
    # Desenhando contador de vidas
    def desenha_vidas(self):
        pygame.font.init()
        fonte = pygame.font.get_default_font()
        fonte_vidas = pygame.font.SysFont(fonte, 90)
        texto_vidas = fonte_vidas.render(str(self.vidas), 1, (255, 0, 0))
        self.tela.blit(texto_vidas, (10, 10))
    
    def desenha_gameover(self):
        self.obstaculo_velocidade = 0
        pygame.font.init()
        fonte = pygame.font.get_default_font()
        fonte_gameover = pygame.font.SysFont(fonte, 90)
        texto_gameover = fonte_gameover.render('GAME OVER', 1, (255, 0, 0))
        fonte_tryagain = pygame.font.SysFont(fonte, 30)
        texto_tryagain = fonte_tryagain.render('ESPACO PARA TENTAR NOVAMENTE', 1, (0, 0, 0))
        self.tela.blit(texto_gameover, (self.largura_tela/2 - texto_gameover.get_width()/2, self.altura_tela/2 - texto_gameover.get_height()/2 -25))
        self.tela.blit(texto_tryagain, (self.largura_tela/2 - texto_tryagain.get_width()/2, self.altura_tela/2 - texto_tryagain.get_height()/2 + 25))
        pygame.display.update()
        self.mover_bg = False                    

    # Redesenhando a tela
    def redesenhar_tela(self):
        if self.mover_bg:
            if self.bg_pos >= self.altura_tela:
                self.bg_pos = -self.altura_tela
            if self.bg_overlap_pos >= self.altura_tela:
                self.bg_overlap_pos = -self.altura_tela

            self.bg_pos += self.bg_speed
            self.bg_overlap_pos += self.bg_speed
            self.tela.blit(self.bg, (0, self.bg_pos))
            self.tela.blit(self.bg_overlap, (0, self.bg_overlap_pos))
            self.tela.blit(self.carro, (self.x, self.y))
            self.desenha_obstaculo(self.obstaculo_x, self.obstaculo_y, self.obstaculo_largura, self.obstaculo_altura, self.obstaculo_cor)
        
        self.tela.blit(self.coracao, (40, 15))
        self.desenha_vidas()
        self.desenha_velocimetro()
        pygame.display.update()

    def run(self):
        while self.jogo_ativo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jogo_ativo = False

            # Game over
            if self.vidas == 0:
                self.desenha_gameover()
                
            # Obstáculos se movendo em direção ao carro
            self.obstaculo_x += int((self.x - self.obstaculo_x) * 0.04)

            # Movimentação do carro
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.x > 0:
                    self.x -= 5
            if keys[pygame.K_RIGHT]:
                if self.x < self.largura_tela - self.carro_largura - 1:
                    self.x += 5

            # Sair do jogo ao apertar esc
            if keys[pygame.K_ESCAPE]:
                pygame.quit()

            # Reiniciar o jogo ao apertar espaço
            if self.obstaculo_velocidade == 0:
                if keys[pygame.K_SPACE]:
                    self.mover_bg = True
                    self.obstaculo_velocidade = self.obstaculo_velocidade_padrao
                    self.obstaculo_x = self.gerando_obstaculos()
                    self.obstaculo_y = -600
                    self.x = (self.largura_tela * 0.45)
                    self.y = (self.altura_tela * 0.8)
                    self.vidas = 3

            
            self.obstaculo_y += self.obstaculo_velocidade
            if self.obstaculo_y > self.altura_tela:
                self.obstaculo_contador += 1
                self.obstaculo_y = 0 - self.obstaculo_altura
                self.obstaculo_x = self.gerando_obstaculos()

            # Colisão com obstáculos
            if (self.obstaculo_y + self.obstaculo_altura) > self.y:
                if self.obstaculo_x > self.x and self.obstaculo_x < self.x + self.carro_largura or \
                        self.obstaculo_x + self.obstaculo_largura > self.x and self.obstaculo_x + self.obstaculo_largura < self.x + self.carro_largura:
                    self.batida_sfx.play()
                    self.vidas -= 1
                    self.obstaculo_x = self.gerando_obstaculos()
                    self.obstaculo_y = -600
                    

            self.redesenhar_tela()
            self.clock.tick(75)

        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
