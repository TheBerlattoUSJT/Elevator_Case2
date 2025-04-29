import pygame
import time

def start_elevator():
    pygame.init()

    # Definindo as dimensões da janela
    WIDTH, HEIGHT = 800, 700
    screen = pygame.display.set_mode((WIDTH + 6, HEIGHT))  # Ajuste no tamanho da janela
    pygame.display.set_caption("Elevador")  # Título da janela

    # Fator de zoom para ajustar as imagens
    zoom_factor = 0.6

    # Função para carregar as imagens e aplicar o zoom
    def load_and_scale_image(path):
        image = pygame.image.load(path)
        new_width = int(WIDTH * zoom_factor)
        new_height = int(HEIGHT * zoom_factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        rect = image.get_rect(center=(WIDTH // 2.5, HEIGHT // 2))
        return image, rect

    # Carregar imagens
    painel_image, painel_rect = load_and_scale_image("case2/painel.jpg")
    ele1_image, ele1_rect = load_and_scale_image("case2/ele1.jpg")
    ele2_image, ele2_rect = load_and_scale_image("case2/ele2.jpg")
    ele3_image, ele3_rect = load_and_scale_image("case2/ele3.jpg")
    porta_aberta, porta_aberta_rect = load_and_scale_image("case2/ele1.jpg")
    porta_fechada, porta_fechada_rect = load_and_scale_image("case2/ele3.jpg")

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (191, 191, 189)

    # Fonte
    font = pygame.font.Font(None, 30)
    font_large = pygame.font.Font(None, 18)
    font_final = pygame.font.Font(None, 50)  # Fonte maior para o texto final

    # Botões
    buttons = {
        "T": pygame.Rect(630, 280, 40, 35),
        "1": pygame.Rect(680, 280, 40, 35),
        "2": pygame.Rect(630, 240, 40, 35),
        "3": pygame.Rect(680, 240, 40, 35),
        "confirmar": pygame.Rect(620, 350, 110, 35),
    }

    # Estado inicial
    pilha_andar = []
    current_screen = "painel"
    andares_clicados = set()

    # Função para exibir os andares
    def exibir_andar(andar_num):
        images = [ele1_image, ele2_image, ele3_image]
        labels = {0: "Térreo", 1: "Andar 1", 2: "Andar 2", 3: "Andar 3"}
        label = labels.get(andar_num, "")

        for img in images:
            screen.fill(WHITE)
            andar_text = font_large.render(label, True, BLACK)
            text_rect = andar_text.get_rect(center=(WIDTH // 3, HEIGHT // 3.2))
            screen.blit(img, img.get_rect(topleft=(ele1_rect.topleft)))
            screen.blit(andar_text, text_rect)
            pygame.display.flip()
            time.sleep(0.3)

    # Função para animar a movimentação do elevador
# Função para animar a movimentação do elevador
    def mover_elevador(andar_destino, _porta_aberta):
        screen.fill(WHITE)
        screen.blit(painel_image, painel_rect.topleft)

        # Mover o elevador até o andar
        if andar_destino == 3:
            screen.blit(ele3_image, ele3_rect.topleft)
            label = "Andar 3"
        elif andar_destino == 2:
            screen.blit(ele2_image, ele2_rect.topleft)
            label = "Andar 2"
        elif andar_destino == 1:
            screen.blit(ele1_image, ele1_rect.topleft)
            label = "Andar 1"
        else:
            screen.blit(ele1_image, ele1_rect.topleft)
            label = "Térreo"

        # Exibir animação das portas
        if _porta_aberta:
            # Porta aberta
            for i in range(5):
                screen.blit(porta_aberta, porta_aberta_rect.topleft)
                pygame.display.flip()
                time.sleep(0.1)
        else:
            # Porta fechada
            for i in range(5):
                screen.blit(porta_fechada, porta_fechada_rect.topleft)
                pygame.display.flip()
                time.sleep(0.1)

        # Mostrar o texto do andar atual
        andar_text = font_large.render(label, True, BLACK)
        text_rect = andar_text.get_rect(center=(WIDTH // 3, HEIGHT // 4))
        screen.blit(andar_text, text_rect)

        pygame.display.flip()
        time.sleep(1)  # Simula a animação da movimentação do elevador

    # Loop principal
    running = True
    while running:
        screen.fill(WHITE)

        if current_screen == "painel":
            screen.blit(painel_image, painel_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for key, rect in buttons.items():
                    if rect.collidepoint(x, y):

                        if key == "confirmar" and pilha_andar:
                            # Confirmação: executa a pilha
                            ultimo_andar = None
                            while pilha_andar:
                                ultimo_andar = pilha_andar.pop()
                                mover_elevador(ultimo_andar, False)  # Começa com as portas fechadas
                                mover_elevador(ultimo_andar, True)  # Começa com as portas fechadas
                                mover_elevador(ultimo_andar, False)  # Começa com as portas fechadas

                            if ultimo_andar is not None:
                                screen.fill(WHITE)
                                if ultimo_andar == 0:
                                    texto_final = "Elevador parado no Térreo"
                                else:
                                    texto_final = f"Elevador parado no Andar {ultimo_andar}"

                                texto_renderizado = font_final.render(texto_final, True, BLACK)
                                screen.blit(texto_renderizado, (WIDTH // 2 - texto_renderizado.get_width() // 2, HEIGHT // 2))
                                pygame.display.flip()
                                time.sleep(2)

                            current_screen = "painel"
                            andares_clicados.clear()

                        elif key in buttons and key != "confirmar" and key not in andares_clicados:
                            if key == "T":
                                pilha_andar.append(0)
                            elif key == "1":
                                pilha_andar.append(1)
                            elif key == "2":
                                pilha_andar.append(2)
                            elif key == "3":
                                pilha_andar.append(3)

                            andares_clicados.add(key)

        # Desenha os botões
        if current_screen == "painel":
            for key, rect in buttons.items():
                if key not in andares_clicados or key == "confirmar":
                    pygame.draw.rect(screen, GREY, rect)
                    texto = "Confirmar" if key == "confirmar" else key
                    text = font.render(texto, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect.topleft)

        pygame.display.flip()
