import pygame
from machine2 import CandyMachine
 
pygame.init()
pygame.mixer.init()
 
WIDTH, HEIGHT = 800, 700  # Ajustando a janela para o tamanho da imagem
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Vending Machine")
 
# Carregando imagem da máquina e som
machine_image = pygame.image.load("media/30751.jpg")
 
# Fator de zoom (quanto maior o valor, maior o zoom)
zoom_factor = 1.2  # Exemplo: 1.0 sem zoom, 1.2 aumenta a imagem em 20%
 
# Redimensiona a imagem com o fator de zoom
machine_image = pygame.transform.scale(
    machine_image, (int(WIDTH * zoom_factor), int(HEIGHT * zoom_factor))
)
 
pygame.mixer.music.load(r"media/som.mp3")
pygame.mixer.music.set_volume(0.5)
 
# Ajustando cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 100)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
GREY = (191, 191, 189)
 
font = pygame.font.Font(None, 20)
 
machine = CandyMachine()
purchased_candy = None
drop_animation = None  
coins = []  # Lista para armazenar animações de moedas
 
# Carregar imagem dos doces e redimensioná-las
candy_images = {
    "A": pygame.image.load("media/refrigerante.jpg"),  
    "B": pygame.image.load("media/chips.jpg"),   
    "C": pygame.image.load("media/biscoito.jpg") 
}
 
# Redimensionando as imagens dos doces (fator de redimensionamento)
candy_size = (40, 40)  # Novo tamanho desejado para as imagens dos doces
candy_images = {key: pygame.transform.scale(image, candy_size) for key, image in candy_images.items()}
 
# Criando botões na área preta da máquina
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
    screen.fill(WHITE)
   
    # Centraliza a imagem de fundo redimensionada
    x_offset = (machine_image.get_width() - WIDTH) // 2
    y_offset = (machine_image.get_height() - HEIGHT) // 2
 
    # Exibe a imagem de fundo com o zoom
    screen.blit(machine_image, (-x_offset, -y_offset))  
   
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
                           
                            # Somente reseta o troco se já houver um valor de troco armazenado
                            if machine.returnChangeBalance > 0:
                                machine.returnChangeBalance = 0  
 
                            machine.insert_money(amount)  
                            pygame.mixer.music.play()  
 
                            coin_x = 650  
                            coin_y = 430  
                            coins.append([coin_x, coin_y, 12])  
                        except ValueError:
                            print(f"Erro ao converter '{key[2:]}' em número")
 
                    elif key in machine.candies:  # Só pode selecionar o doce se o estado for "Selecting"
                        if machine.current_state != "Selecting":
                            print("Erro: Insira o dinheiro primeiro!")
                        else:
                            purchased_candy = key  # Atualiza o doce comprado
                            machine.select_candy(key)  
                            pygame.mixer.music.play()  # Toca o som ao selecionar o doce
                            drop_animation = {"x": 300, "y": 500, "image": candy_images[key]}  # Inicializa animação da queda
 
    # Exibir saldo
    balance_text = font.render(f"Saldo: R$ {machine.balance:.2f}", True, BLACK)
    screen.blit(balance_text, (586, 75))
 
    # Exibir valores válidos
    valid_money_label = font.render("Valores válidos", True, WHITE)
    screen.blit(valid_money_label, (585, 120))
 
    # Exibir tipos de doces
    candy_type_label = font.render("Tipos de doce", True, WHITE)
    screen.blit(candy_type_label, (586, 260))
 
    # Exibir troco (se houver)
    if machine.returnChangeBalance != 0:
        return_change = font.render(f"Troco: R$ {machine.returnChangeBalance:.2f}", True, BLACK)
        screen.blit(return_change, (587, 95))
 
    # Exibir animação de queda do doce
    if drop_animation:
        screen.blit(drop_animation["image"], (drop_animation["x"], drop_animation["y"]))
        drop_animation["y"] += 0.7  # Faz a imagem cair
        if drop_animation["y"] >= 600:  # Ponto final da queda
            drop_animation = None
 
   
 
    # Animação das moedas subir
    y_min = 380
 
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin[0], coin[1]), coin[2])  
        if coin[1] > y_min:  # Só move a moeda se ela ainda não atingiu o limite superior
            coin[1] -= 1
        else:
            coins.remove(coin)
 
    # Desenhando botões
    for key, rect in buttons.items():
        pygame.draw.rect(screen, GREY, rect)
        text = font.render(key, True, BLACK)
 
        # Centraliza o texto dentro do botão
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect.topleft)
 
    pygame.display.flip()
 
pygame.quit()