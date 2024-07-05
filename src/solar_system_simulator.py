import pygame
import subprocess

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import glm
import numpy as np
import os


def go_back():
    subprocess.Popen(["python", "opengl project/src/presentacion.py"])
    pygame.quit()
    


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Configurar la luz
    light_position = [0.0, 0.0, 0.0, 1.0]  # Posición del sol
    light_color = [1.0, 1.0, 1.0, 1.0]  # Color de la luz (blanco)
    ambient_light = [0.1, 0.1, 0.1, 1.0]  # Luz ambiental

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)


    


class Camera:
    def __init__(self, width, height, position, skybox_size):
        self.Position = glm.vec3(position)
        self.Orientation = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3(0.0, 1.0, 0.0)
        self.cameraMatrix = glm.mat4(1.0)
        self.firstClick = True
        self.width = width
        self.height = height
        self.speed = 0.1
        self.sensitivity = 200.0  # Incrementar la sensibilidad para un movimiento más rápido
        self.skybox_size = skybox_size

    def update_matrix(self, FOVdeg, near_plane, far_plane):
        view = glm.lookAt(self.Position, self.Position + self.Orientation, self.Up)
        projection = glm.perspective(glm.radians(FOVdeg), self.width / self.height, near_plane, far_plane)
        self.cameraMatrix = projection * view

    def matrix(self):
        return np.array(self.cameraMatrix.to_list(), dtype=np.float32)

    def inputs(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            new_position = self.Position + self.speed * self.Orientation
            if self.is_within_bounds(new_position):
                self.Position = new_position
        if keys[K_a]:
            new_position = self.Position + self.speed * -glm.normalize(glm.cross(self.Orientation, self.Up))
            if self.is_within_bounds(new_position):
                self.Position = new_position
        if keys[K_s]:
            new_position = self.Position + self.speed * -self.Orientation
            if self.is_within_bounds(new_position):
                self.Position = new_position
        if keys[K_d]:
            new_position = self.Position + self.speed * glm.normalize(glm.cross(self.Orientation, self.Up))
            if self.is_within_bounds(new_position):
                self.Position = new_position

        if keys[K_LCTRL]:
            new_position = self.Position + self.speed * -self.Up
            if self.is_within_bounds(new_position):
                self.Position = new_position
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

    def is_within_bounds(self, position):
        limit = self.skybox_size - 1  # Limitar a un poco menos que el tamaño del skybox
        return -limit <= position.x <= limit and -limit <= position.y <= limit and -limit <= position.z <= limit

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

    # Back
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
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

def draw_orbit(radius, segments=100):
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0.0, z)
    glEnd()

def draw_rings(inner_radius, outer_radius, segments=100):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        x = math.cos(theta)
        z = math.sin(theta)
        glTexCoord2f(i / segments, 1)
        glVertex3f(outer_radius * x, 0.0, outer_radius * z)
        glTexCoord2f(i / segments, 0)
        glVertex3f(inner_radius * x, 0.0, inner_radius * z)
    glEnd()

def draw_cube(size, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    # Front face
    glTexCoord2f(0, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    # Back face
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, -size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
    # Left face
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(-size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
    # Right face
    glTexCoord2f(0, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(size, size, -size)
    # Top face
    glTexCoord2f(0, 0); glVertex3f(-size, size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    # Bottom face
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, -size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, -size, size)
    glEnd()

def music():
    pygame.mixer.init()
    pygame.mixer.music.load('OPENGL PROJECT/sounds/relax.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(2000)  # Espera 2 segundos antes de continuar con el bucle principal

def main():
    pygame.init()
    
    # Obtener la información de la pantalla
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    
    # Configurar la pantalla con la resolución obtenida
    display = (width, height)
    pygame.display.set_caption("Solar System by PG")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)

    skybox_size = 30 # Define el tamaño del skybox
    camera = Camera(display[0], display[1], [0.0, 0.0, 10.0], skybox_size)  # Crear la cámara

    sun_texture_id = load_texture("OPENGL PROJECT/image/suns.jpg")
    planet1_texture_id = load_texture("OPENGL PROJECT/image/mercu.jpg")
    planet2_texture_id = load_texture("OPENGL PROJECT/image/venus.jpg")
    planet3_texture_id = load_texture("OPENGL PROJECT/image/earth.jpg")
    planet4_texture_id = load_texture("OPENGL PROJECT/image/mars.jpg")
    planet5_texture_id = load_texture("OPENGL PROJECT/image/jupiter.jpg")
    planet6_texture_id = load_texture("OPENGL PROJECT/image/saturn.jpg")
    planet7_texture_id = load_texture("OPENGL PROJECT/image/uranus.jpg")
    planet8_texture_id = load_texture("OPENGL PROJECT/image/neptune.jpg")
    ring_texture_id = load_texture("OPENGL PROJECT/image/rings.jpg")  # los anillos de Saturno
    skybox_texture = load_texture("OPENGL PROJECT/skybox/stars.jpg")   #textura del skybox

    
    cube_texture_ids = [  # texturas para los cubos de cada planeta
    load_texture("OPENGL PROJECT/image/mertx.jpg"),
    load_texture("OPENGL PROJECT/image/venutx.jpg"),
    load_texture("OPENGL PROJECT/image/earthtx.jpg"),
    load_texture("opengl project/image/martx.jpg"),
    load_texture("opengl project/image/juptx.jpg"),
    load_texture("opengl project/image/sattx.jpg"),
    load_texture("opengl project/image/uratx.jpg"),
    load_texture("opengl project/image/neptx.jpg")
    ]


    # Cargar texturas
    models_folder = 'opengl project/modelo'
    obj_files = ['Satellite.obj']
    obj_textures_folder = 'opengl project/modelo/Textures/'

    obj_textures = load_textures_from_folder(obj_textures_folder)
    loaded_models = {}

    for obj_file in obj_files:
        obj_filename = os.path.join(models_folder, obj_file)
        vertices, faces, tex_coords, material_indices = load_obj(obj_filename)
        loaded_models[obj_file] = (vertices, faces, tex_coords, material_indices)
    angle = 0
    clock = pygame.time.Clock()

    satellite_speed_multiplier = 14 # Ajusta este valor para aumentar la velocidad del satélite
    satellite_angle = 0.0   

    animation_running = True  # Bandera para controlar si la animación está en curso
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    animation_running = not animation_running  # Alternar la bandera de animación
                if event.key == pygame.K_ESCAPE:  # Verificar si se presionó la tecla ESCAPE
                    go_back()

        camera.inputs()  # Actualizar inputs de la cámara
        camera.update_matrix(60.0, 0.1, 50.0)  # Actualizar matriz de la cámara

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(camera.matrix())  # Cargar la matriz de la cámara

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar el skybox
        draw_skybox(skybox_size, skybox_texture)

        # Dibujar el sol
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, sun_texture_id)
        draw_sphere(3.0, 30, 30, sun_texture_id)
        glPopMatrix()

        # Dibujar los planetas girando alrededor del sol y sus órbitas
        planet_distances = [6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
        planet_textures = [planet1_texture_id, planet2_texture_id, planet3_texture_id, planet4_texture_id, planet5_texture_id, planet6_texture_id, planet7_texture_id, planet8_texture_id]
        planet_sizes = [0.3, 0.4, 0.5, 0.45, 1.0, 0.9, 0.6, 0.55]
        planet_speeds = [4, 2.8, 2.6, 2.4, 2.2, 2, 1.8, 1.6]

        for i in range(len(planet_distances)):
            glPushMatrix()
            # Dibujar la órbita
            glColor3f(1.0, 1.0, 1.0)
            draw_orbit(planet_distances[i])
            glPopMatrix()

        if animation_running:
            angle += 0.01  # Incrementar el ángulo para la animación de los planetas
            satellite_angle += 0.1 * satellite_speed_multiplier  # Incrementar el ángulo del satélite de forma independiente

        for i in range(len(planet_distances)):
            glPushMatrix()
            glRotatef(angle * planet_speeds[i], 0, 1, 0)
            glTranslatef(planet_distances[i] * math.cos(angle * planet_speeds[i]), 0.0,
                         planet_distances[i] * math.sin(angle * planet_speeds[i]))
            glBindTexture(GL_TEXTURE_2D, planet_textures[i])
            draw_sphere(planet_sizes[i], 20, 20, planet_textures[i])
            if i == 5:  # Añadir anillos para el sexto planeta (Saturno)
                glBindTexture(GL_TEXTURE_2D, ring_texture_id)
                glPushMatrix()
                glRotatef(45, 1, 0, 0)  # Rotar los anillos 45 grados alrededor del eje x
                draw_rings(1.02 * planet_sizes[i], 1.3 * planet_sizes[i])
                glPopMatrix()
            glPopMatrix()

        # Dibujar el modelo Satellite.obj girando alrededor del sol
        glPushMatrix()
        glRotatef(-satellite_angle, 0, 1, 0)  # Girar en la dirección opuesta a los planetas con mayor velocidad
        glTranslatef(9.0, 0.0, 2.0)  # Mover al lado derecho del sol
        glScalef(0.02, 0.02, 0.02)  # Escalar para hacerlo más pequeño
        draw_obj(loaded_models['Satellite.obj'][0], loaded_models['Satellite.obj'][1], loaded_models['Satellite.obj'][2], loaded_models['Satellite.obj'][3], obj_textures)
        glPopMatrix()

        # Dibujar un cuadro encima de cada planeta con la etiqueta correspondiente
        for i in range(len(planet_distances)):
            glPushMatrix()
            glRotatef(angle * planet_speeds[i], 0, 1, 0)
            glTranslatef(planet_distances[i] * math.cos(angle * planet_speeds[i]), 1.3,  # Mover 1.5 unidades en el eje Y para posicionar encima del planeta
                         planet_distances[i] * math.sin(angle * planet_speeds[i]))
            draw_cube(0.3, cube_texture_ids[i])  # Dibujar un cubo más pequeño
            glPopMatrix()

        pygame.display.flip()

        clock.tick(120)  

if __name__ == "__main__":
    music()  # Reproducir música
    main()   # Iniciar el bucle principal del programa
