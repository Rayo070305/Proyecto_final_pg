import pygame
import sys
import subprocess
from pygame import mixer

# Inicializar Pygame
pygame.init()
mixer.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sistema Solar")

# Cargar la imagen de fondo
background_image = pygame.image.load("skybox/space3.jpg").convert()

# Colores del botón
button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)
button_pressed_color = (50, 50, 50)

# Dimensiones y posición de los botones
button_width, button_height = 200, 60
button_margin = 20  # Aumentar margen para mayor separación
column_margin = 50  # Margen entre columnas
buttons = []
planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
icons = [f"icons/{planet.lower()}.png" for planet in planets]

# Calcular la posición de las columnas
column1_x = (width // 2) - column_margin - button_width
column2_x = (width // 2) + column_margin

# Calcular la posición inicial vertical para centrar los botones
total_height = (len(planets) // 2) * (button_height + button_margin) - button_margin
start_y = (height - total_height) // 2

for i, planet in enumerate(planets):
    col = i % 2
    row = i // 2
    x = column1_x if col == 0 else column2_x
    y = start_y + (row * (button_height + button_margin))
    button_rect = pygame.Rect(x, y, button_width, button_height)
    icon_image = pygame.image.load(icons[i]).convert_alpha()
    icon_image = pygame.transform.scale(icon_image, (30, 30))
    buttons.append((button_rect, planet, icon_image))

# Añadir botón de volver
back_button_rect = pygame.Rect(10, height - 60, 100, 40)
back_button_text = "Volver"
back_button_font = pygame.font.Font(None, 30)
back_button_surface = back_button_font.render(back_button_text, True, (255, 255, 255))
back_button_text_rect = back_button_surface.get_rect(center=back_button_rect.center)

# Fuente y texto de los botones
font = pygame.font.Font(None, 36)

# Función para abrir el otro script
def open_planet_script(planet):
    script_name = f"src/{planet.lower()}_simulator.py"
    subprocess.Popen(["python", script_name])
    pygame.quit()

# Función para manejar el botón de volver
def go_back():
    # Aquí puedes definir lo que debe hacer el botón de volver
    pygame.quit()

# Cargar el sonido de clic
click_sound = mixer.Sound('sounds/click.mp3')

# Bucle principal del juego
running = True
button_pressed = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_rect, planet, icon in buttons:
                if button_rect.collidepoint(event.pos):
                    button_pressed = planet
                    click_sound.play()
            if back_button_rect.collidepoint(event.pos):
                button_pressed = "back"
                click_sound.play()
        if event.type == pygame.MOUSEBUTTONUP:
            if button_pressed:
                if button_pressed == "back":
                    go_back()
                else:
                    for button_rect, planet, icon in buttons:
                        if button_rect.collidepoint(event.pos) and button_pressed == planet:
                            open_planet_script(planet)
                button_pressed = None

    # Dibujar la imagen de fondo
    screen.blit(background_image, (0, 0))

    for button_rect, planet, icon in buttons:
        if button_pressed == planet:
            pygame.draw.rect(screen, button_pressed_color, button_rect)
        else:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(screen, button_color, button_rect)

        text_surface = font.render(planet, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(button_rect.centerx + 15, button_rect.centery))
        
        screen.blit(icon, (button_rect.x + 10, button_rect.y + (button_height - icon.get_height()) // 2))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

    # Dibujar el botón de volver
    if button_pressed == "back":
        pygame.draw.rect(screen, button_pressed_color, back_button_rect)
    else:
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, back_button_rect)
        else:
            pygame.draw.rect(screen, button_color, back_button_rect)
    
    screen.blit(back_button_surface, back_button_text_rect)
    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2)

    # Actualizar la pantalla
    pygame.display.flip()
