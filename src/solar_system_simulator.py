import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame import mixer
import math

def music():
    mixer.init()
    mixer.music.load('OPENGL PROJECT/sounds/relax.mp3')
    mixer.music.play()
    # Espera 5 segundos antes de continuar con el bucle principal
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


def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_caption("Sytem solar by PG")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)




    sun_texture_id = load_texture("OPENGL PROJECT/image/suns.jpg")
    planet1_texture_id = load_texture("OPENGL PROJECT/image/mars4k.jpg")
    planet2_texture_id = load_texture("OPENGL PROJECT/image/venus.jpg")
    planet3_texture_id = load_texture("OPENGL PROJECT/image/earth.jpg")
    planet4_texture_id = load_texture("OPENGL PROJECT/image/neptune.jpg")
    planet5_texture_id = load_texture("OPENGL PROJECT/image/jupiter.jpg")
    planet6_texture_id = load_texture("OPENGL PROJECT/image/saturn.jpg")
    angle = 0  # Una sola variable de ángulo para la rotación
    music()
    mouse_prev_pos = None
    mouse_pressed = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Rueda de scroll hacia arriba
                    glTranslatef(0, 0, 1)
                elif event.button == 5:  # Rueda de scroll hacia abajo
                    glTranslatef(0, 0, -1)
                elif event.button == 1:  # B.otón izquierdo del ratón
                    mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and mouse_pressed:
                if mouse_prev_pos is not None:
                    dx, dy = event.rel
                    glTranslatef(dx / 40, -dy / 40, 0)
                mouse_prev_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0, 1)
                elif event.key == pygame.K_DOWN:
                    glTranslatef(0, 0, -1)
                elif event.key == pygame.K_LEFT:
                    glTranslatef(1, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    glTranslatef(-1, 0, 0)

        angle += 0.1  # Velocidad de rotación lenta y pareja

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
         # Cargar textura del skybox
        glPushMatrix()
        skybox_texture = load_texture("OPENGL PROJECT/skybox/sta.jpg")
        glBindTexture(GL_TEXTURE_2D, skybox_texture)
        glPopMatrix()
        # Dibujar el skybox

        draw_skybox(20, skybox_texture)


        # Dibujar el sol
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, sun_texture_id)
        draw_sphere(3.0, 30, 30, sun_texture_id)
        glPopMatrix()


        # Dibujar los planetas girando alrededor del sol
        planet_distances = [2.0, 4.0, 5.0, 8.0, 10.0, 12.0]
        planet_textures = [planet1_texture_id, planet2_texture_id, planet3_texture_id, planet4_texture_id, planet5_texture_id, planet6_texture_id]
        planet_sizes = [0.3, 0.4, 0.5, 0.5, 0.5, 0.5]

        for i in range(len(planet_distances)):
            glPushMatrix()
            glRotatef(angle + i * 45, 0, 1, 0)  # Desfase de ángulo para que giren uno detrás del otro
            glTranslatef(planet_distances[i], 0.0, 0.0)
            glBindTexture(GL_TEXTURE_2D, planet_textures[i])
            draw_sphere(planet_sizes[i], 20, 20, planet_textures[i])
            glPopMatrix()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()