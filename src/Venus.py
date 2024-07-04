import pygame
import math
import subprocess
import sys

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Información sobre Venus')

# Cargar imagen de fondo
background_image = pygame.image.load("opengl project/skybox/sta.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)

# Centro del círculo
center = (width // 2, height // 2)

# Radio del círculo (se ha reducido a la mitad)
radius = min(width, height) // 6

# Cargar la imagen de Mercurio
image = pygame.image.load("opengl project/image/venus.jpg")
original_rect = image.get_rect()

# Escalar la imagen para que se ajuste al círculo
image = pygame.transform.scale(image, (2 * radius, 2 * radius))

# Crear una máscara circular
mask = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)

# Cargar la imagen del meteorito
meteorito_image = pygame.image.load("opengl project/image/asteorid.png")
meteorito_image = pygame.transform.scale(meteorito_image, (100, 100))  # Ajusta el tamaño según sea necesario

# Posición del meteorito en la esquina superior derecha
meteorito_rect = meteorito_image.get_rect(topright=(width - 10, 10))

# Definir el área del botón
button_rect = pygame.Rect(10, 10, 100, 50)

# Crear textos para la parte izquierda
texts = ["",
    "-------INFORMACION SOBRE VENUS------:",
    "","",
    "Composición: Principalmente roca y metal.",
    
    "Temperatura de la superficie: Alrededor de 465°C.",
    
    "Diámetro: Aproximadamente 12,104 kilómetros.",
    
    "Distancia a la Tierra: Varía entre 38 y 261 millones de kilómetros.",
    
    "Edad: Formado hace unos 4.5 mil millones de años.",
    
    "Masa: Aproximadamente 0.82 veces la masa de la Tierra.",
    "Vida útil: existirá mientras dure el sistema solar", "aproximadamente otros 5 mil millones de años.",
    
    "Curiosidad: Tiene una rotación retrógrada, gira en sentido contrario a la mayoría de los planetas."
]

font = pygame.font.SysFont(None, 25)
text_surfaces = [font.render(text, True, WHITE) for text in texts]

clock = pygame.time.Clock()

# Función para abrir la ventana anterior
def open_previous_window():
    subprocess.Popen(["python", "opengl project/src/planets_menu.py"])
    pygame.quit()
    sys.exit()

# Variables para la rotación
angulo_planeta = 0
velocidad_rotacion = 1.0

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

    # Dibujar imagen del meteorito en la esquina superior derecha
    screen.blit(meteorito_image, meteorito_rect)

    # Calcular la rotación del planeta
    angulo_planeta += velocidad_rotacion
    imagen_rotada = pygame.transform.rotate(image, angulo_planeta)
    imagen_rect = imagen_rotada.get_rect(center=(center[0] + 280, center[1]))

    # Dibujar la imagen de Mercurio dentro del círculo usando la máscara
    masked_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
    masked_image.blit(imagen_rotada, (imagen_rect.x - (center[0] + 280 - radius), imagen_rect.y - (center[1] - radius)))
    masked_image.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    screen.blit(masked_image, (center[0] + 280 - radius, center[1] - radius))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
