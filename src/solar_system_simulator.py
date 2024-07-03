import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import glm
import numpy as np
import os

class Camera:
    def _init_(self, width, height, position):
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
            self.speed = 1.0
        else:
            self.speed = 1.0

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

def load_textures_from_folder(folder_path):
    textures = []

    files = os.listdir(folder_path)
    image_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    for file in image_files:
        file_path = os.path.join(folder_path, file)
        texture_id = load_texture(file_path)
        textures.append(texture_id)

    return textures

def load_obj(filename):
    vertices = []
    faces = []
    tex_coords = []
    material_indices = []

    current_material_index = -1

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith('f '):
                face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                faces.append(face)
                material_indices.append(current_material_index)
            elif line.startswith('vt '):
                tex_coords.append(list(map(float, line.strip().split()[1:3])))
            elif line.startswith('usemtl '):
                material_name = line.strip().split()[1]
                if material_name.startswith('texture'):
                    current_material_index = int(material_name[len('texture'):]) - 1
                else:
                    current_material_index = -1

    return vertices, faces, tex_coords, material_indices

def draw_obj(vertices, faces, tex_coords, material_indices, textures):
    glEnable(GL_TEXTURE_2D)

    for i, face in enumerate(faces):
        material_index = material_indices[i]
        if material_index >= 0 and material_index < len(textures):
            glBindTexture(GL_TEXTURE_2D, textures[material_index])

        glBegin(GL_TRIANGLES)
        for vertex_index in face:
            glTexCoord2f(tex_coords[vertex_index][0], tex_coords[vertex_index][1])
            glVertex3fv(vertices[vertex_index])
        glEnd()

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

def music():
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/relax.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(2000)  # Espera 2 segundos antes de continuar con el bucle principal

def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_caption("Solar System by PG")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)

    camera = Camera(display[0], display[1], [0.0, 0.0, 10.0])  # Crear la cámara

    sun_texture_id = load_texture("image/suns.jpg")
    planet1_texture_id = load_texture("image/mars4k.jpg")
    planet2_texture_id = load_texture("image/venus.jpg")
    planet3_texture_id = load_texture("image/earth.jpg")
    planet4_texture_id = load_texture("image/neptune.jpg")
    planet5_texture_id = load_texture("image/jupiter.jpg")
    planet6_texture_id = load_texture("image/saturn.jpg")
    planet7_texture_id = load_texture("image/uranus.jpg")
    planet8_texture_id = load_texture("image/mer1.jpg")
    skybox_texture = load_texture("skybox/sta.jpg")

    # Cargar modelos OBJ
    models_folder = 'modelo'
    obj_files = ['Satellite.obj']  # Lista de archivos OBJ a cargar
    obj_textures_folder = 'modelo/Textures/'

    # Cargar texturas de la carpeta de texturas de modelos
    obj_textures = load_textures_from_folder(obj_textures_folder)

    # Diccionario para almacenar los modelos cargados
    loaded_models = {}

    for obj_file in obj_files:
        obj_filename = os.path.join(models_folder, obj_file)
        vertices, faces, tex_coords, material_indices = load_obj(obj_filename)
        loaded_models[obj_file] = (vertices, faces, tex_coords, material_indices)

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
        planet_distances = [2.0, 4.0, 5.0, 8.0, 10.0, 12.0, 14.0, 16.0]
        planet_textures = [planet1_texture_id, planet2_texture_id, planet3_texture_id, planet4_texture_id,
                           planet5_texture_id, planet6_texture_id, planet7_texture_id, planet8_texture_id]
        planet_sizes = [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3]

        for i in range(len(planet_distances)):
            glPushMatrix()
            glRotatef(angle + i * 45, 0, 1, 0)  # Desfase de ángulo para que giren uno detrás del otro
            glTranslatef(planet_distances[i], 0.0, 0.0)
            glBindTexture(GL_TEXTURE_2D, planet_textures[i])
            draw_sphere(planet_sizes[i], 20, 20, planet_textures[i])
            glPopMatrix()

        # Dibujar el modelo Satellite.obj girando alrededor del sol
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)  # Girar junto con los planetas
        glTranslatef(0.0, 0.0, -6.0)  # Mover al lado derecho del sol
        glScalef(0.02, 0.02, 0.02)  # Escalar para hacerlo más pequeño
        draw_obj(loaded_models['Satellite.obj'][0], loaded_models['Satellite.obj'][1], loaded_models['Satellite.obj'][2], loaded_models['Satellite.obj'][3], obj_textures)
        glPopMatrix()

        pygame.display.flip()
        angle += 0.1  # Incrementar el ángulo para la animación
        clock.tick(60)  # Asegurar 60 FPS

if _name_ == "_main_":
    music()  # Reproducir música
    main()   # Iniciar el bucle principal del programa