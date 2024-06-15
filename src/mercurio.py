import pygame
import math
import subprocess
import sys

pygame.init()

# Dimensiones de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('informacion mercurio')

# Cargar imagen de fondo
background_image = pygame.image.load("skybox/space3.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)

# Centro del círculo
center = (width // 2, height // 2)

# Radio del círculo (se ha reducido a la mitad)
radius = min(width, height) // 6

# Cargar la imagen del sol
image = pygame.image.load("pg_project/image/mercury.jpg")
original_rect = image.get_rect()

# Escalar la imagen para que se ajuste al círculo
image = pygame.transform.scale(image, (2 * radius, 2 * radius))

# Crear una máscara circular
mask = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)

# Definir el área del botón
button_rect = pygame.Rect(10, 10, 100, 50)

# Crear textos para la parte izquierda
texts = [
    "-------INFORMACION SOBRE MERCURIO------:",
    "",
    "Composición: Principalmente roca y metal.",
    "",
    "Temperatura de la superficie: Varía entre -173°C y más de 427°C.",
    "",
    "Diámetro: Aproximadamente 4,880 kilómetros.",
    "",
    "Distancia a la Tierra: Varía entre 77 y 222 millones de kilómetros.",
    "",
    "Edad: Formado hace unos 4.5 mil millones de años.",
    "",
    "Masa: Cerca de 0.06 veces la masa de la Tierra.",
    "",
    "Vida útil: No aplica como en las estrellas.",
    "",
    "Curiosidad: Es el planeta más cercano al Sol y tiene la órbita más excéntrica del sistema solar."
]

font = pygame.font.SysFont(None, 25)
text_surfaces = [font.render(text, True, WHITE) for text in texts]

clock = pygame.time.Clock()

# Función para abrir la ventana anterior
def open_previous_window():
    subprocess.Popen(["python", "src/planets_menu.py"])
    pygame.quit()
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verificar si se hace clic en el botón
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                open_previous_window()

    # Dibujar fondo
    screen.blit(background_image, (0, 0))

    # Dibujar el botón
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.SysFont(None, 30)
    text = font.render("Regresar", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # Dibujar textos en la parte izquierda (movidos hacia abajo)
    for i, text_surface in enumerate(text_surfaces):
        screen.blit(text_surface, (20, 90 + i * 30))

    # Dibujar la imagen dentro del círculo usando la máscara
    masked_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
    masked_image.blit(image, (0, 0))
    masked_image.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    screen.blit(masked_image, (center[0] + 280 - radius, center[1] - radius))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
