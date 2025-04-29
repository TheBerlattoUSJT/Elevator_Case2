import pygame
import sys

# Importar os módulos dos dois cases
import case1_machine
import case2_elevator

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Cases")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (191, 191, 189)

font = pygame.font.Font(None, 48)

# Botões para selecionar os cases
button_case1 = pygame.Rect(300, 250, 200, 60)
button_case2 = pygame.Rect(300, 350, 200, 60)

running = True
while running:
    screen.fill(WHITE)

    title = font.render("Escolha um Case", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    # Desenha botões
    pygame.draw.rect(screen, GREY, button_case1)
    pygame.draw.rect(screen, GREY, button_case2)

    text_case1 = font.render("Case 1", True, BLACK)
    text_case2 = font.render("Case 2", True, BLACK)

    screen.blit(text_case1, (button_case1.x + 40, button_case1.y + 10))
    screen.blit(text_case2, (button_case2.x + 40, button_case2.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_case1.collidepoint(x, y):
                case1_machine.run_case1()
            elif button_case2.collidepoint(x, y):
                case2_elevator.run_case2()

    pygame.display.flip()

pygame.quit()
sys.exit()