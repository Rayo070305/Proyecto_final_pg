import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import glm
import numpy as np
from pygame import mixer

def music():
    mixer.init()
    mixer.music.load('sounds/relax.mp3')
    mixer.music.play()
    pygame.time.delay(2000)  # Espera 2 segundos antes de continuar con el bucle principal

class Camera:
    def __init__(self, width, height, position):
        self.Position = glm.vec3(position)
        self.Orientation = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3(0.0, 1.0, 0.0)
        self.cameraMatrix = glm.mat4(1.0)
        self.firstClick = True
        self.width = width
        self.height = height
        self.speed = 0.1
        self.sensitivity = 100.0

    def update_matrix(self, FOVdeg, near_plane, far_plane):
        view = glm.lookAt(self.Position, self.Position + self.Orientation, self.Up)
        projection = glm.perspective(glm.radians(FOVdeg), self.width / self.height, near_plane, far_plane)
        self.cameraMatrix = projection * view

    def matrix(self):
        return np.array(self.cameraMatrix.to_list(), dtype=np.float32)

    def inputs(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.Position += self.speed * self.Orientation
        if keys[K_a]:
            self.Position += self.speed * -glm.normalize(glm.cross(self.Orientation, self.Up))
        if keys[K_s]:
            self.Position += self.speed * -self.Orientation
        if keys[K_d]:
            self.Position += self.speed * glm.normalize(glm.cross(self.Orientation, self.Up))
        if keys[K_SPACE]:
            self.Position += self.speed * self.Up
        if keys[K_LCTRL]:
            self.Position += self.speed * -self.Up
        if keys[K_LSHIFT]:
            self.speed = 0.4
        else:
            self.speed = 0.1

        if pygame.mouse.get_pressed()[0]:
            pygame.mouse.set_visible(False)
            if self.firstClick:
                pygame.mouse.set_pos(self.width // 2, self.height // 2)
                self.firstClick = False

            mouse_x, mouse_y = pygame.mouse.get_pos()
            rot_x = self.sensitivity * (mouse_y - self.height // 2) / self.height
            rot_y = self.sensitivity * (mouse_x - self.width // 2) / self.width

            new_orientation = glm.rotate(self.Orientation, glm.radians(-rot_x), glm.normalize(glm.cross(self.Orientation, self.Up)))

            angle_between = glm.degrees(glm.acos(glm.dot(glm.normalize(new_orientation), glm.normalize(self.Up))))
            if abs(angle_between - 90.0) <= 85.0:
                self.Orientation = new_orientation

            self.Orientation = glm.rotate(self.Orientation, glm.radians(-rot_y), self.Up)

            pygame.mouse.set_pos(self.width // 2, self.height // 2)
        else:
            pygame.mouse.set_visible(True)
            self.firstClick = True

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
    pygame.display.set_caption("Solar System by PG")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)

    camera = Camera(display[0], display[1], [0.0, 0.0, -10.0])  # Crear la cámara

    sun_texture_id = load_texture("image/suns.jpg")
    planet1_texture_id = load_texture("image/mars4k.jpg")
    planet2_texture_id = load_texture("image/venus.jpg")
    planet3_texture_id = load_texture("image/earth.jpg")
    planet4_texture_id = load_texture("image/neptune.jpg")
    planet5_texture_id = load_texture("image/jupiter.jpg")
    planet6_texture_id = load_texture("image/saturn.jpg")
    skybox_texture = load_texture("skybox/sta.jpg")

    angle = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        camera.inputs()  # Actualizar inputs de la cámara
        camera.update_matrix(60.0, 0.1, 50.0)  # Actualizar matriz de la cámara

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(camera.matrix())  # Cargar la matriz de la cámara

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar el skybox
        draw_skybox(20, skybox_texture)

        # Dibujar el sol
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, sun_texture_id)
        draw_sphere(3.0, 30, 30, sun_texture_id)
        glPopMatrix()

        # Dibujar los planetas girando alrededor del sol
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
        angle += 0.1  # Incremento de ángulo para la animación
        clock.tick(60)  # Asegurar 60 FPS

if __name__ == "__main__":
    music()  # Reproducir música
    main()   # Iniciar el bucle principal del programa

