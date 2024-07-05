import pygame
import sys
import subprocess
from pygame import mixer

# Inicializar Pygame
pygame.init()
mixer.init()

# Configuración de la pantalla
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sistema Solar")

# Cargar la imagen de fondo
background_image = pygame.image.load("opengl project/skybox/sta.jpg").convert()

# Colores del botón
button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)
button_pressed_color = (50, 50, 50)

# Dimensiones y posición de los botones
button_width, button_height = 200, 60
button_margin = 20  # Aumentar margen para mayor separación
column_margin = 50  # Margen entre columnas
buttons = []
celestial_objects = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
icons = [f"opengl project/icons/{obj.lower()}.png" for obj in celestial_objects]

# Calcular la posición de las columnas
column1_x = (width // 2) - column_margin - button_width
column2_x = (width // 2) + column_margin

# Calcular la posición inicial vertical para centrar los botones
total_height = (len(celestial_objects) // 2) * (button_height + button_margin) - button_margin
start_y = (height - total_height) // 2

for i, obj in enumerate(celestial_objects):
    col = i % 2
    row = i // 2
    if obj == "Neptune":
        x = (column1_x + column2_x) // 2  # Centrar entre las dos columnas
    else:
        x = column1_x if col == 0 else column2_x
    y = start_y + (row * (button_height + button_margin))
    button_rect = pygame.Rect(x, y, button_width, button_height)
    icon_image = pygame.image.load(icons[i]).convert_alpha()
    icon_image = pygame.transform.scale(icon_image, (30, 30))
    buttons.append((button_rect, obj, icon_image))

# Añadir botón de volver
back_button_width, back_button_height = 100, 40
back_button_rect = pygame.Rect(0, height - back_button_height, back_button_width, back_button_height)
back_button_text = "Volver"
back_button_font = pygame.font.Font(None, 30)
back_button_surface = back_button_font.render(back_button_text, True, (255, 255, 255))
back_button_text_rect = back_button_surface.get_rect(center=back_button_rect.center)

# Fuente y texto de los botones
font = pygame.font.Font(None, 36)

# Función para abrir el otro script
def open_script(celestial_object):
    if celestial_object == "Sun":
        script_name = "opengl project/src/sol.py"
    elif celestial_object == "Mercury":
        script_name = "opengl project/src/Mercurio.py"
    elif celestial_object == "Venus":
        script_name = "opengl project/src/Venus.py"
    elif celestial_object == "Earth":
        script_name = "opengl project/src/Tierra.py"
    elif celestial_object == "Mars":
        script_name = "opengl project/src/Marte.py"
    elif celestial_object == "Jupiter":
        script_name = "opengl project/src/Jupiter.py"
    elif celestial_object == "Saturn":
        script_name = "opengl project/src/Saturno.py"
    elif celestial_object == "Uranus":
        script_name = "opengl project/src/Urano.py"
    elif celestial_object == "Neptune":
        script_name = "opengl project/src/Neptuno.py"
    else:
        script_name = f"opengl project/src/{celestial_object.lower()}_simulator.py"
    subprocess.Popen(["python", script_name])
    pygame.quit()

# Función para manejar el botón de volver
def go_back():
    subprocess.Popen(["python", "opengl project/src/presentacion.py"])
    pygame.quit()
    sys.exit()

# Cargar el sonido de clic
click_sound = mixer.Sound('opengl project/sounds/click.mp3')

# Bucle principal del juego
running = True
button_pressed = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_rect, celestial_object, icon in buttons:
                if button_rect.collidepoint(event.pos):
                    button_pressed = celestial_object
                    click_sound.play()
            if back_button_rect.collidepoint(event.pos):
                button_pressed = "back"
                click_sound.play()
        if event.type == pygame.MOUSEBUTTONUP:
            if button_pressed:
                if button_pressed == "back":
                    go_back()
                else:
                    for button_rect, celestial_object, icon in buttons:
                        if button_rect.collidepoint(event.pos) and button_pressed == celestial_object:
                            open_script(celestial_object)
                button_pressed = None

    # Dibujar la imagen de fondo
    screen.blit(background_image, (0, 0))

    for button_rect, celestial_object, icon in buttons:
        if button_pressed == celestial_object:
            pygame.draw.rect(screen, button_pressed_color, button_rect)
        else:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(screen, button_color, button_rect)

        text_surface = font.render(celestial_object, True, (255, 255, 255))
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

pygame.quit()
sys.exit()
