import pygame
import sys
import json
from game import iniciar_jogo

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Menu do Jogo')

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregar imagem de fundo
background_img = pygame.image.load('img/menu.jpg').convert_alpha()  # Substitua pelo caminho para a sua imagem de fundo

# Fonte
menu_font = pygame.font.Font('crackman/Crackman.otf', 60)  # Fonte maior para o título do menu
button_font = pygame.font.Font('crackman/Crackman Front.otf', 48)  # Fonte menor para os botões

# Função para desenhar o texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Função para criar botões com texto
def draw_text_button(text, x, y, width, height, font, action=None):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, button_rect, 2)  # Borda preta
    draw_text(text, font, WHITE, screen, x + width // 2, y + height // 2)  # Desenha o texto sobre o botão
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()
    return button_rect.collidepoint(mouse)

# Função para ler rankings
def read_rankings():
    try:
        with open('rank.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para escrever rankings
def write_rankings(rankings):
    with open('rank.json', 'w') as file:
        json.dump(rankings, file, indent=4)

# Função para salvar o nome e rank
def salvar_nome_e_rank(nome, vitoria):
    # Cria um dicionário com o nome e o rank
    dados = {'nome': nome, 'rank': vitoria}

    # Salva os dados no arquivo JSON
    with open('rank.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)



# Função principal do menu
def menu():
    input_box = pygame.Rect(150, 200, 150, 32)  # Ajustado para a tela menor
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()
    nome_salvo = False  # Flag para garantir que o nome só é salvo uma vez

    while True:
        screen.blit(background_img, (0, 0))  # Desenha o fundo

        draw_text('GAME FILO', menu_font, WHITE, screen, screen_width // 2, 50)

        # Exibindo o campo de texto para o nome
        txt_surface = button_font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        if draw_text_button('Iniciar', 150, 280, 200, 50, button_font, action=lambda: iniciar_jogo()):
            if not nome_salvo and text:
                salvar_nome_e_rank(text, 0)
                nome_salvo = True  # Garantir que o nome seja salvo apenas uma vez

        if draw_text_button('Rank', 175, 340, 150, 50, button_font, action=lambda: print('Exibir Ranking')):
            pass

        if draw_text_button('Quit', 175, 400, 150, 50, button_font, action=lambda: pygame.quit() or sys.exit()):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not nome_salvo and text:
                        salvar_nome_e_rank(text, 0)
                        nome_salvo = True
                    text = ''
                    active = False
                    color = color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

        pygame.display.flip()
        clock.tick(30)

menu()
