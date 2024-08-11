import pygame
import random
from config import *
pygame.init()
from dados_json import *

from essential_functions import *
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
# Função para manter a janela sempre no topo da barra de tarefas
x_pos = 0
y_pos = screen_height - HEIGHT - 40
ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, x_pos, y_pos, 0, 0, 0x0001)


# Carregar imagens
ship_img = pygame.image.load("img/ship_1.png").convert_alpha()
ship_img = pygame.transform.scale(ship_img, (30, 30))
alien_img1 = pygame.image.load("img/aliens/alien1.png").convert_alpha()  # Tipo 1
alien_img1 = pygame.transform.scale(alien_img1, (20, 30))
alien_img2 = pygame.image.load("img/aliens/alien2.png").convert_alpha()  # Tipo 2
alien_img2 = pygame.transform.scale(alien_img2, (20, 30))
alien_img3 = pygame.image.load("img/aliens/alien3.png").convert_alpha()  # Tipo 3
alien_img3 = pygame.transform.scale(alien_img3, (20, 30))
alien_img4 = pygame.image.load("img/aliens/alien4.png").convert_alpha()  # Tipo 4
alien_img4 = pygame.transform.scale(alien_img4, (20, 30))

item_img1 = pygame.image.load("img/itens/healt.png").convert_alpha()  # Item tipo 1 healt
item_img1 = pygame.transform.scale(item_img1, (15, 15))
item_img2 = pygame.image.load("img/itens/escudo.png").convert_alpha()  # Item tipo 2 escudo
item_img2 = pygame.transform.scale(item_img2, (15, 15))
item_img3 = pygame.image.load("img/itens/laser.png").convert_alpha()  # Item tipo 3 laser
item_img3 = pygame.transform.scale(item_img3, (15, 15))
item_img4 = pygame.image.load("img/itens/misseis_item.png").convert_alpha()  # Item tipo 4 missies
item_img4 = pygame.transform.scale(item_img4, (15, 15))

item_images = [item_img1, item_img2, item_img3, item_img4]  # Lista de imagens de itens colecionáveis
background = pygame.image.load('img/img_menu.jpg').convert_alpha()

# Obter a largura da imagem de fundo
background_width = background.get_width()
# Calcular o número de repetições necessárias para cobrir a largura da tela
num_repeats = (WIDTH // background_width) + 1

# Configurações da nave
ship_width, ship_height = ship_img.get_size()
ship_pos = [50, HEIGHT // 2 - ship_height // 2]
ship_speed = 5#velocidade da nave do player

# Configurações dos projéteis
bullet_width = 5
bullet_height = 1
bullets = []
bullet_speed = 10
#config dos missil
missile_img = pygame.image.load("img/itens/misseis.png").convert_alpha()
missile_img = pygame.transform.scale(missile_img, (20, 5))

# Adicione as variáveis para os mísseis
missiles = []
MAX_MISSILES = 3
missile_speed = 7
explosions = []
explosion_radius_increment = 2
max_explosion_radius = 50  # Tamanho máximo da explosão

######################
# Configurações dos alienígenas
alien_speed = 1.5
alien_types = [alien_img1, alien_img2, alien_img3, alien_img4]  # Lista de tipos de alienígenas
alien_death_threshold = [1, 1,1, 1]  # Número de mortes necessárias para deixar o item

aliens = []
alien_width, alien_height = alien_img1.get_size()

# Configurações dos itens colecionáveis
item_width, item_height = item_img1.get_size()
items = []

# Configurações do escudo
shield_active = False
shield_duration = 50  # Duração do escudo em frames
shield_timer = 0

# Configurações do laser
laser_active = False
laser_duration = 100  # Duração do laser em frames
laser_timer = 0
laser_pos = None  # Inicializar como None
laser_speed = 5  # Velocidade do laser

# Configurações do relógio
clock = pygame.time.Clock()



# Função para detectar colisão
def detect_collision(obj1_pos, obj2_pos, obj1_width, obj1_height, obj2_width, obj2_height):
    o1_x, o1_y = obj1_pos
    o2_x, o2_y = obj2_pos

    if (o1_x < o2_x + obj2_width) and (o1_x + obj1_width > o2_x) and (o1_y < o2_y + obj2_height) and (
            o1_y + obj1_height > o2_y):
        return True
    return False

def draw_explosions():
    for explosion in explosions[:]:
        pygame.draw.circle(screen, RED, explosion["pos"], explosion["radius"], 2)
        explosion["radius"] += explosion_radius_increment
        if explosion["radius"] > max_explosion_radius:
            check_explosion_hits(explosion)
            explosions.remove(explosion)

# Função para verificar se a explosão atingiu algum alienígena
def check_explosion_hits(explosion):
    for alien in aliens[:]:
        alien_center = (alien["pos"][0] + alien_width // 2, alien["pos"][1] + alien_height // 2)
        distance = pygame.math.Vector2(alien_center).distance_to(explosion["pos"])
        if distance <= explosion["radius"]:
            aliens.remove(alien)
            global score
            score += 1
# Função para gerar item colecionável
def generate_item_type(alien_type_index):
    return item_images[alien_type_index]  # Escolhe o item correspondente ao tipo de alienígena

def game_over_screen():
    global game_over, score
    game_over = True
    font = pygame.font.SysFont(None, 25)

    while game_over:
        screen.fill(BLACK)
        draw_text('Game Over!', font, RED, screen, WIDTH // 2 - 50, HEIGHT // 2 )
        draw_text('Press R to Restart or Q to Quit', font, RED, screen, WIDTH // 2 - 120, HEIGHT // 2 - 20)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Sai do jogo completamente
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()  # Função para reiniciar o jogo
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Sai do jogo completamente

def restart_game():
    global game_over, score, aliens, bullets, items, ship_pos, shield_active, shield_timer, laser_active, laser_timer, laser_pos, missiles, explosions, missile_enabled

    # Reinicializar variáveis principais
    game_over = False
    score = 0
    aliens = []
    bullets = []
    items = []
    missiles = []
    explosions = []

    # Redefinir a posição inicial da nave
    ship_pos = [50, HEIGHT // 2 - ship_img.get_height() // 2]

    # Reiniciar estados e temporizadores
    shield_active = False
    shield_timer = 0
    laser_active = False
    laser_timer = 0
    laser_pos = None
    missile_enabled = False  # Desativar o disparo de mísseis

    # Outras variáveis globais que possam ser afetadas pelo estado do jogo podem ser redefinidas aqui, se necessário.


def pause():
    paused = True
    font = pygame.font.SysFont(None, 30)
    draw_text('Paused. Press P to continue.', font, RED, screen, WIDTH // 2 - 100, HEIGHT // 2 - 10)
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(5)

# Loop principal do jogo
missile_enabled = False
game_over = False
paused = False
score = 0

# Fonte para o texto do score e game over
font = pygame.font.SysFont(None, 15)
def main():
    #player_name = get_player_name()  # Obter o nome do jogador antes de iniciar o jogo
    global missile_enabled, game_over, score, aliens, bullets, items, ship_pos, shield_active, shield_timer, laser_active, laser_timer, laser_pos
    caminho_json = 'pontuacoes.json'
    nome_jogador = get_player_name(screen)
    verificar_ou_criar_json(caminho_json)


    while not game_over:
        """ mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x <= WIDTH and 0 <= mouse_y <= HEIGHT:
            paused = False
        else:
            paused = True"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:

                    pause()
                elif event.key == pygame.K_SPACE:
                    bullet_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2 - bullet_height // 2]
                    bullets.append(bullet_pos)
                elif (event.key == pygame.K_LCTRL):
                    pygame.quit()
                    exit()

                elif event.key == pygame.K_z and laser_active:  # Disparar o laser
                    laser_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2]
                    laser_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2]
                elif event.key == pygame.K_m and missile_enabled:  # Disparar o míssil
                    missile_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2 ]
                    missiles.append(missile_pos)
        keys = pygame.key.get_pressed()
        if not paused:
            if keys[pygame.K_UP] and ship_pos[1] > 0:
                ship_pos[1] -= ship_speed
            if keys[pygame.K_DOWN] and ship_pos[1] < HEIGHT - ship_height:
                ship_pos[1] += ship_speed
            if keys[pygame.K_LEFT] and ship_pos[0] > 0:
                ship_pos[0] -= ship_speed
            if keys[pygame.K_RIGHT] and ship_pos[0] < WIDTH - ship_width:
                ship_pos[0] += ship_speed

        screen.fill(BLACK)
        #para add fundo a largura da janela
        for i in range(num_repeats):
            screen.blit(background, (i * background_width, 0))

        # Movimentação dos projéteis
        for bullet in bullets[:]:
            bullet[0] += bullet_speed
            if bullet[0] > WIDTH:
                bullets.remove(bullet)

        # Adicionar alienígenas
        if random.randint(1, 20) == 1:
            alien_type_index = random.randint(0, len(alien_types) - 1)
            alien_pos = [WIDTH - alien_img1.get_width(), random.randint(0, HEIGHT - alien_img1.get_height())]
            aliens.append({"pos": alien_pos, "type": alien_type_index, "death_count": 0})

        # Movimentação dos alienígenas
        for alien in aliens[:]:
            alien["pos"][0] -= alien_speed
            if alien["pos"][0] < 0:
                aliens.remove(alien)

        # Detecção de colisão entre projéteis e alienígenas
        for bullet in bullets[:]:
            bullet_removed = False
            for alien in aliens[:]:
                if detect_collision(bullet, alien["pos"], bullet_width, bullet_height, alien_width, alien_height):
                    if bullet in bullets:  # Verificar se o projétil ainda está na lista
                        bullets.remove(bullet)
                        bullet_removed = True
                    alien["death_count"] += 1
                    if alien["death_count"] >= alien_death_threshold[alien["type"]]:
                        aliens.remove(alien)
                        # Incrementar o score ao destruir o alienígena
                        score += 1
                        # Adicionar item colecionável ao ser destruído
                        item_type = generate_item_type(alien["type"])
                        item_pos = alien["pos"]
                        items.append({"pos": item_pos, "type": item_type})
                if bullet_removed:
                    break

        # Movimentação dos itens colecionáveis
        for item in items[:]:
            item["pos"][0] #-= alien_speed
            if item["pos"][0] < 0:
                items.remove(item)

        #colisao da nave com aliens
        for alien in aliens[:]:
            if detect_collision(ship_pos, alien["pos"], ship_width, ship_height, alien_width, alien_height):
                if shield_active:
                    # Se o escudo estiver ativo, não termine o jogo
                    aliens.remove(alien)
                    score += 1
                else:
                    game_over = True

        # Detecção de colisão entre nave e itens colecionáveis
        for item in items[:]:
            if detect_collision(ship_pos, item["pos"], ship_width, ship_height, item_width, item_height):
                if item["type"] == item_img2:  # Se o item for do tipo "escudo"
                    shield_active = True
                    shield_timer = shield_duration
                if item["type"] == item_img3:  # Se o item for do tipo "laser"
                    laser_active = True
                    laser_timer = laser_duration

                if item['type'] == item_img4:
                    missile_enabled = True  # Ativa a capacidade de disparar mísseis
                    # Remova o item coletado

                items.remove(item)

        # Atualizar e desenhar projéteis na tela
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

        #detectar colisao dos misseis com aliens
        for missile in missiles[:]:
            missile[0] += missile_speed
            if missile[0] > WIDTH:
                missiles.remove(missile)
                continue  # Pular o resto do loop para este míssil

            missile_removed = False
            for alien in aliens[:]:
                if detect_collision(missile, alien["pos"], 20, 10, alien_width, alien_height):
                    explosions.append({"pos": (missile[0], missile[1]), "radius": 0})
                    score += 1
                    missiles.remove(missile)
                    missile_removed = True
                    break  # Sai do loop de alienígenas se o míssil colidir com um alienígena

            if missile_removed:
                break  # Sai do loop de mísseis se um míssil for removido

            # Se o número de mísseis exceder o limite, remova os mais antigos
            if len(missiles) >= MAX_MISSILES:
                missile_enabled = False



            # Desenhar alienígenas na tela
        for alien in aliens:
            screen.blit(alien_types[alien["type"]], alien["pos"])

        #desenhar missies na tela
        for missile in missiles:
            screen.blit(missile_img, missile)

        # Desenhar itens colecionáveis na tela
        for item in items:
            screen.blit(item["type"], item["pos"])

        # Desenhar a nave
        screen.blit(ship_img, ship_pos)

        # Desenhar o escudo redondo
        if shield_active:
            pygame.draw.circle(screen, BLUE, (ship_pos[0] + ship_width // 2, ship_pos[1] + ship_height // 2),
                               max(ship_width, ship_height) // 2 + 10, 2)
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        # Desenhar o laser, se o laser estiver ativo e laser_pos não for None
        if laser_active and laser_pos:
            # Atualizar a posição do laser
            laser_pos[0] += laser_speed
            laser_rect = pygame.Rect(laser_pos[0], 0, 2, HEIGHT)
            pygame.draw.rect(screen, RED, laser_rect)

            # Verificar colisão do laser com os alienígenas
            for alien in aliens[:]:
                if laser_rect.colliderect(
                        pygame.Rect(alien["pos"][0], alien["pos"][1], alien_width, alien_height)):
                    aliens.remove(alien)
                    score += 1

            # Verificar se o laser saiu da tela
            if laser_pos[0] > WIDTH:
                laser_active = False
                laser_pos = None  # Redefinir laser_pos para None quando o laser acabar

            laser_timer -= 1
            if laser_timer <= 0:
                laser_active = False
                laser_pos = None  # Redefinir laser_pos para None quando o laser acabar

        draw_explosions()#desenhar explosao ao collidir misseis com aliens

        # Mostrar o score na tela
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
        #atualizar pontucao no .json
        atualizar_pontuacao(caminho_json, nome_jogador, score)
        # Mostrar mensagem de Game Over se o jogo terminar
        if game_over:
            game_over_screen()

        pygame.display.flip()
        clock.tick(60)

    # Encerrar o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()