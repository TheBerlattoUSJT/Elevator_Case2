import pygame
from case1.machine2 import CandyMachine

def start_vending_machine():
    pygame.init()
    pygame.mixer.init()

    # Tamanho da tela
    WIDTH, HEIGHT = 800, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Inicializando a tela
    pygame.display.set_caption("Candy Vending Machine")

    # Carregar imagem da máquina e som
    machine_image = pygame.image.load("case1/media/30751.jpg")
    zoom_factor = 1.2
    machine_image = pygame.transform.scale(
        machine_image, (int(WIDTH * zoom_factor), int(HEIGHT * zoom_factor))
    )

    pygame.mixer.music.load(r"case1/media/som.mp3")
    pygame.mixer.music.set_volume(0.5)

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 215, 0)
    GREY = (191, 191, 189)

    font = pygame.font.Font(None, 20)

    machine = CandyMachine()
    purchased_candy = None
    drop_animation = None
    coins = []

    # Carregar imagens dos doces
    candy_images = {
        "A": pygame.image.load("case1/media/refrigerante.jpg"),
        "B": pygame.image.load("case1/media/chips.jpg"),
        "C": pygame.image.load("case1/media/biscoito.jpg")
    }
    candy_size = (40, 40)
    candy_images = {key: pygame.transform.scale(img, candy_size) for key, img in candy_images.items()}

    buttons = {
        "R$ 1": pygame.Rect(585, 140, 90, 35),
        "R$ 2": pygame.Rect(585, 176, 90, 35),
        "R$ 5": pygame.Rect(585, 212, 90, 35),
        "A": pygame.Rect(582, 282, 50, 50),
        "B": pygame.Rect(633, 282, 50, 50),
        "C": pygame.Rect(582, 333, 100, 50)
    }

    running = True
    while running:
        screen.fill(WHITE)  # Preenchendo a tela com a cor branca

        x_offset = (machine_image.get_width() - WIDTH) // 2
        y_offset = (machine_image.get_height() - HEIGHT) // 2
        screen.blit(machine_image, (-x_offset, -y_offset))  # Desenhando a imagem da máquina

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for key, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        if key in ["R$ 1", "R$ 2", "R$ 5"]:
                            try:
                                amount = float(key[2:].replace(',', '.').strip())

                                if machine.returnChangeBalance > 0:
                                    machine.returnChangeBalance = 0

                                machine.insert_money(amount)
                                pygame.mixer.music.play()

                                coin_x = 650
                                coin_y = 430
                                coins.append([coin_x, coin_y, 12])

                            except ValueError:
                                print(f"Erro ao converter '{key[2:]}' em número")

                        elif key in machine.candies:
                            if machine.current_state != "Selecting":
                                print("Erro: Insira o dinheiro primeiro!")
                            else:
                                purchased_candy = key
                                machine.select_candy(key)
                                pygame.mixer.music.play()
                                drop_animation = {"x": 300, "y": 500, "image": candy_images[key]}

        # Exibir saldo
        balance_text = font.render(f"Saldo: R$ {machine.balance:.2f}", True, BLACK)
        screen.blit(balance_text, (586, 75))

        valid_money_label = font.render("Valores válidos", True, WHITE)
        screen.blit(valid_money_label, (585, 120))

        candy_type_label = font.render("Tipos de doce", True, WHITE)
        screen.blit(candy_type_label, (586, 260))

        if machine.returnChangeBalance != 0:
            return_change = font.render(f"Troco: R$ {machine.returnChangeBalance:.2f}", True, BLACK)
            screen.blit(return_change, (587, 95))

        if drop_animation:
            screen.blit(drop_animation["image"], (drop_animation["x"], drop_animation["y"]))
            drop_animation["y"] += 0.7
            if drop_animation["y"] >= 600:
                drop_animation = None

        y_min = 380
        for coin in coins[:]:
            pygame.draw.circle(screen, YELLOW, (coin[0], coin[1]), coin[2])
            if coin[1] > y_min:
                coin[1] -= 1
            else:
                coins.remove(coin)

        for key, rect in buttons.items():
            pygame.draw.rect(screen, GREY, rect)
            text = font.render(key, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect.topleft)

        pygame.display.flip()  # Atualizando a tela
