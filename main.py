import pygame
import random
import ctypes

# Inicialização do Pygame
pygame.init()

# Configurações da tela
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
WIDTH, HEIGHT = screen_width, 50  # Largura ajustada para ocupar toda a largura da tela

# Configura a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Invasão Alienígena")

# Posicionar a janela do jogo acima da barra de tarefas
x_pos = 0
y_pos = screen_height - HEIGHT - 40
ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, x_pos, y_pos, 0, 0, 0x0001)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Carregar imagens
ship_img = pygame.image.load("img/ship_1.png").convert_alpha()
ship_img = pygame.transform.scale(ship_img, (30, 30))
############## Aliens###################
alien_img1 = pygame.image.load("img/alien1.png").convert_alpha()  # Tipo 1
alien_img1 = pygame.transform.scale(alien_img1, (20, 30))
alien_img2 = pygame.image.load("img/alien2.png").convert_alpha()  # Tipo 2
alien_img2 = pygame.transform.scale(alien_img2, (20, 30))
alien_img3 = pygame.image.load("img/alien3.png").convert_alpha()  # Tipo 3
alien_img3 = pygame.transform.scale(alien_img3, (20, 30))
alien_img4 = pygame.image.load("img/alien4.png").convert_alpha()  # Tipo 4
alien_img4 = pygame.transform.scale(alien_img4, (20, 30))
###################### itens ###########################
item_img1 = pygame.image.load("img/healt.png").convert_alpha()  # Item tipo 1
item_img1 = pygame.transform.scale(item_img1, (15, 15))
item_img2 = pygame.image.load("img/escudo.png").convert_alpha()  # Item tipo 2
item_img2 = pygame.transform.scale(item_img2, (15, 15))
item_img3 = pygame.image.load("img/healt.png").convert_alpha()  # Item tipo 3
item_img3 = pygame.transform.scale(item_img3, (15, 15))
item_img4 = pygame.image.load("img/item4.png").convert_alpha()  # Item tipo 4
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
ship_speed = 5

# Configurações dos projéteis
bullet_width = 5
bullet_height = 5
bullets = []
bullet_speed = 10

# Configurações dos alienígenas
alien_speed = 1.5
alien_types = [alien_img1, alien_img2, alien_img3, alien_img4]  # Lista de tipos de alienígenas
alien_death_threshold = [3, 5, 7, 3]  # Número de mortes necessárias para deixar o item

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
laser_speed  = 5  # Velocidade do laser

# Configurações do relógio
clock = pygame.time.Clock()

# Função para desenhar texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Função para detectar colisão
def detect_collision(obj1_pos, obj2_pos, obj1_width, obj1_height, obj2_width, obj2_height):
    o1_x, o1_y = obj1_pos
    o2_x, o2_y = obj2_pos

    if (o1_x < o2_x + obj2_width) and (o1_x + obj1_width > o2_x) and (o1_y < o2_y + obj2_height) and (
            o1_y + obj1_height > o2_y):
        return True
    return False

# Função para gerar item colecionável
def generate_item_type(alien_type_index):
    return item_images[alien_type_index]  # Escolhe o item correspondente ao tipo de alienígena

# Loop principal do jogo
game_over = False
paused = False
score = 0

# Fonte para o texto do score e game over
font = pygame.font.SysFont(None, 15)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2 - bullet_height // 2]
                bullets.append(bullet_pos)
            if (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and pygame.key.get_pressed()[pygame.K_x]:
                game_over = True
            if event.key == pygame.K_z and laser_active:  # Disparar o laser
                laser_pos = [ship_pos[0] + ship_width, ship_pos[1] + ship_height // 2]

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
        item["pos"][0] -= alien_speed
        if item["pos"][0] < 0:
            items.remove(item)
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
            if item["type"] == item_img4:  # Se o item for do tipo "laser"
                laser_active = True
                laser_timer = laser_duration
            items.remove(item)

    # Atualizar e desenhar projéteis na tela
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Desenhar alienígenas na tela
    for alien in aliens:
        screen.blit(alien_types[alien["type"]], alien["pos"])

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
        pygame.draw.rect(screen, GREEN, laser_rect)

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

    # Mostrar o score na tela
    draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)

    # Mostrar mensagem de Game Over se o jogo terminar
    if game_over:
        draw_text('Game Over!', font, RED, screen, WIDTH // 2 - 50, HEIGHT // 2 - 15)

    pygame.display.flip()
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()
