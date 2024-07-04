import pygame
import sys
import subprocess
from pygame import mixer
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicializar Pygame y el mezclador de sonido
pygame.init()
mixer.init()

def music():
    mixer.init()
    mixer.music.load('opengl project/sounds/relax.mp3')
    mixer.music.play(-1)  # Loop the music indefinitely

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texture_id, width, height

def draw_sphere(radius, slices, stacks, texture_id):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluSphere(quad, radius, slices, stacks)

def draw_skybox(size, texture):
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Front
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, -size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
    glEnd()

    # Left
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(-size, size, -size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    glEnd()

    # Right
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(size, size, -size)
    glEnd()

    # Top
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    glEnd()

    # Bottom
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, -size, -size)
    glTexCoord2f(0, 1); glVertex3f(-size, -size, -size)
    glEnd()

    glPopMatrix()
    glDisable(GL_LIGHTING)
    glDepthMask(GL_TRUE)

def open_previous_window():
    subprocess.Popen(["python", "opengl project/src/planets_menu.py"])
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_caption("Sistema Solar Educativo")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    
    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    planet_texture_id = load_texture("opengl project/image/mars.jpg")[0]
    info_texture_id, info_width, info_height = load_texture("opengl project/image/informacionmarte.jpg")
    skybox_texture_id, _, _ = load_texture("opengl project/skybox/sta.jpg")
    return_button_texture_id, return_button_width, return_button_height = load_texture("opengl project/image/volver2.png")

    # Escalar la imagen del botón "volver"
    scaled_button_width = return_button_width // 2
    scaled_button_height = return_button_height // 2

    angle = 0
    music()

    clock = pygame.time.Clock()

    # Cargar el sonido de clic
    click_sound = mixer.Sound('opengl project/sounds/click.mp3')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the mouse click is within the bounds of the return button
                    mouse_x, mouse_y = event.pos
                    button_top_left_x = 0
                    button_top_left_y = 0
                    button_bottom_right_x = scaled_button_width
                    button_bottom_right_y = scaled_button_height
                    if button_top_left_x <= mouse_x <= button_bottom_right_x and \
                       button_top_left_y <= mouse_y <= button_bottom_right_y:
                        click_sound.play()
                        open_previous_window()

        angle += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Dibujar el skybox como fondo
        draw_skybox(20.0, skybox_texture_id)
        
        # Dibujar el planeta en la parte derecha
        glPushMatrix()
        glTranslatef(3, 0, 0)  # Mover el planeta a la derecha
        glRotatef(angle, 0, 1, 0)
        glBindTexture(GL_TEXTURE_2D, planet_texture_id)
        draw_sphere(2.5, 30, 30, planet_texture_id)
        glPopMatrix()

        # Configurar vista ortográfica para dibujar la imagen de información
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], 0, display[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Centrar verticalmente y desplazar hacia la derecha
        info_x = 150  # Ajusta la posición X de la imagen de información
        info_y = (display[1] - info_height) / 2  # Centra verticalmente
        glBindTexture(GL_TEXTURE_2D, info_texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(info_x, info_y)
        glTexCoord2f(1, 0)
        glVertex2f(info_x + info_width, info_y)
        glTexCoord2f(1, 1)
        glVertex2f(info_x + info_width, info_y + info_height)
        glTexCoord2f(0, 1)
        glVertex2f(info_x, info_y + info_height)
        glEnd()

        # Dibujar el botón de "volver" un poco más a la derecha desde la esquina superior izquierda
        button_offset_x = 10  # Ajuste horizontal
        button_offset_y = -10  # Ajuste vertical
        glBindTexture(GL_TEXTURE_2D, return_button_texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(button_offset_x, display[1] - scaled_button_height + button_offset_y)
        glTexCoord2f(1, 0); glVertex2f(button_offset_x + scaled_button_width, display[1] - scaled_button_height + button_offset_y)
        glTexCoord2f(1, 1); glVertex2f(button_offset_x + scaled_button_width, display[1] + button_offset_y)
        glTexCoord2f(0, 1); glVertex2f(button_offset_x, display[1] + button_offset_y)
        glEnd()

        # Restaurar la matriz de proyección original
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
