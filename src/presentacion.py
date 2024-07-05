import pygame
import sys
import subprocess
from pygame import mixer

# Inicializar Pygame y el mezclador de sonido
pygame.init()
mixer.init()

# Definir el tamaño de la ventana
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

# Cargar la imagen de fondo y ajustarla al tamaño de la ventana
background_image = pygame.image.load("opengl project/image/presentacion.jpeg").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Definir el color del botón
button_color = (100, 100, 100)

# Fuente para los botones
font = pygame.font.Font(None, 36)

# Crear una función para ajustar el tamaño del botón en función del texto
def create_button(text, x, y, padding_x=20, padding_y=10):
    text_surface = font.render(text, True, (255, 255, 255))
    button_width = text_surface.get_width() + padding_x * 2
    button_height = text_surface.get_height() + padding_y * 2
    button_rect = pygame.Rect(x, y, button_width, button_height)
    return button_rect, text_surface

# Ajuste de la posición de los botones
offset_x = 50  # Cambiar este valor para mover los botones más a la izquierda

# Botón "Simulacion sistema solar!" en la esquina superior derecha
button_text = "Simulacion sistema solar!"
button_rect, button_text_surface = create_button(button_text, width - 300 - offset_x, 20)

# Botón de información en la esquina inferior derecha
info_button_text = "Información de los planetas"
info_button_rect, info_text_surface = create_button(info_button_text, width - 300 - offset_x, height - 70)

# Botón de salir en la esquina inferior izquierda
exit_button_text = "Salir"
exit_button_rect, exit_text_surface = create_button(exit_button_text, 20, height - 70)

# Función para abrir el otro script
def open_solar_system():
    subprocess.Popen(["python", "opengl project/src/solar_system_simulator.py"])
    pygame.quit()
    sys.exit()

def open_planets_menu():
    subprocess.Popen(["python", "opengl project/src/planets_menu.py"])
    pygame.quit()
    sys.exit()

# Cargar el sonido de clic
click_sound = mixer.Sound('opengl project/sounds/click.mp3')

# Estado del juego
state = "main"

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "main":
                if button_rect.collidepoint(event.pos):
                    state = "instructions"
                    click_sound.play()
                elif info_button_rect.collidepoint(event.pos):
                    open_planets_menu()
                    click_sound.play()
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
                    click_sound.play()
            elif state == "instructions":
                if exit_button_rect.collidepoint(event.pos):
                    running = False
                    click_sound.play()
                elif start_simulation_button_rect.collidepoint(event.pos):
                    open_solar_system()

    # Dibujar según el estado del juego
    if state == "main":
        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Dibujar el botón "Simulacion sistema solar!"
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
        screen.blit(button_text_surface, button_rect.move(20, 10))

        # Dibujar el botón de información
        pygame.draw.rect(screen, button_color, info_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), info_button_rect, 2)
        screen.blit(info_text_surface, info_button_rect.move(20, 10))

        # Dibujar el botón de salir
        pygame.draw.rect(screen, button_color, exit_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
        screen.blit(exit_text_surface, exit_button_rect.move(20, 10))
    elif state == "instructions":
        
        # Dibujar la pantalla de instrucciones
        screen.fill((0, 0, 0))
        instructions = [
            "NOTA IMPORTANTE",
            "Se mueve con las teclas W,A,S,D,SPACE Y Ctrl",
            "La cámara se controla con el mouse",
            "Para salir de la simulacion presione la tecla ESC",
            "Haga clic en 'Iniciar Simulación' para comenzar"
        ]
        y_offset = height // 3
        for instruction in instructions:
            instruction_text = font.render(instruction, True, (255, 255, 255))
            screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, y_offset))
            y_offset += 50

        # Botón para iniciar la simulación
        start_simulation_text = "Iniciar Simulación"
        start_simulation_button_rect, start_simulation_text_surface = create_button(start_simulation_text, width // 2 - 150, y_offset + 50)  # Ajustar la posición

        # Dibujar el botón para iniciar la simulación
        pygame.draw.rect(screen, button_color, start_simulation_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), start_simulation_button_rect, 2)
        screen.blit(start_simulation_text_surface, start_simulation_button_rect.move(20, 10))

        # Dibujar el botón de salir
        pygame.draw.rect(screen, button_color, exit_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
        screen.blit(exit_text_surface, exit_button_rect.move(20, 10))

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
