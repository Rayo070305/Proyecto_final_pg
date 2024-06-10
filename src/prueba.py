import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame import mixer
import math

def music():
    mixer.init()
    mixer.music.load('sounds/relax.mp3')
    mixer.music.play()
    pygame.time.delay(2000)

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
    return texture_id

def draw_sphere(radius, slices, stacks, texture_id):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluSphere(quad, radius, slices, stacks)

def draw_text(x, y, text, font_size=24):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    # Guardar el estado actual de OpenGL
    glPushAttrib(GL_ALL_ATTRIB_BITS)

    # Configurar para dibujar el texto
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1280, 0, 720)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Dibujar el texto
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # Restaurar el estado anterior de OpenGL
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopAttrib()

def display_info():
    info = [
        "Planeta: Marte",
        "Diámetro: 6,779 km",
        "Masa: 6.39 × 10^23 kg",
        "Gravedad: 3.721 m/s²",
        "Órbita: 687 días terrestres"
    ]
    y = 680
    for line in info:
        draw_text(20, y, line)
        y -= 30

def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_caption("Sistema Solar Educativo")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    
    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    planet_texture_id = load_texture("image/mars4k.jpg")
    angle = 0
    music()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        angle += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Dibujar el planeta
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glBindTexture(GL_TEXTURE_2D, planet_texture_id)
        draw_sphere(2.0, 30, 30, planet_texture_id)
        glPopMatrix()
        
        # Dibujar la información
        display_info()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()