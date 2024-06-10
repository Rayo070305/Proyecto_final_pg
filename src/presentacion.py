import pygame
import sys
import subprocess
from pygame import mixer

# Inicializar Pygame y el mezclador de sonido
pygame.init()
mixer.init()

# Definir el tamaño de la ventana
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# Cargar la imagen de fondo y ajustarla al tamaño de la ventana
background_image = pygame.image.load("image/presentacion.png").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Definir el color del botón y el fondo del listado
button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)
list_background_color = (50, 50, 50)

# Calcular las dimensiones y posiciones de los botones en función del tamaño de la ventana
button_width = width // 5
button_height = height // 15
button_x = width // 10
button_y = (height - button_height) // 2

info_button_width = width // 5
info_button_height = height // 15
info_button_x = width * 7 // 9
info_button_y = button_y - height // 2.2

# Crear el rectángulo del primer botón
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Fuente y texto del primer botón
font = pygame.font.Font(None, 36)
button_text = font.render("Click Me!", True, (255, 255, 255))
text_rect = button_text.get_rect(center=button_rect.center)

# Crear el rectángulo del segundo botón (botón de información)
info_button_rect = pygame.Rect(info_button_x, info_button_y, info_button_width, info_button_height)



# Función para abrir el otro script
def open_solar_system():
    subprocess.Popen(["python", "src/solar_system_simulator.py"])
    pygame.quit()
    sys.exit()
    




# Bucle principal del juego
info_display = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                open_solar_system()


    # Dibujar la imagen de fondo
    screen.blit(background_image, (0, 0))

    # Dibujar el primer botón
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    screen.blit(button_text, text_rect)

    # Dibujar el segundo botón (botón de información)
    pygame.draw.rect(screen, button_color, info_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), info_button_rect, 2)
    screen.blit(font.render("Información", True, (255, 255, 255)), info_button_rect.topleft)


    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
