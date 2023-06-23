import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time
import numpy as np
import os

def init():
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Galaxies in OpenGL!")

    gluPerspective(45, display[0] / display[1], 0.1, 1000.0)
    glTranslatef(0.0, 0.0, -100.0)  # Adjust the translation to move the galaxies away from the viewer

    # Toggle fullscreen
    pygame.key.set_repeat(1, 10)

def generate_galaxies(num_galaxies, cluster_size=100, void_size=1000):
    galaxies = np.zeros((num_galaxies, 6), dtype=np.float32)
    centers = np.random.uniform(-100, 100, (num_galaxies // cluster_size, 3)).astype(np.float32)

    for i in range(num_galaxies):
        cluster_idx = i // cluster_size

        if cluster_idx % void_size == 0:
            galaxies[i, 0:3] = np.random.uniform(-100, 100, 3).astype(np.float32)
        else:
            center = centers[cluster_idx]
            offset = np.random.uniform(-10, 10, 3).astype(np.float32)
            galaxies[i, 0:3] = center + offset

        # Assign specific colors to each galaxy
        brightness = np.random.uniform(0.5, 1.0)  # generate random brightness
        if i % 10 == 0 or i % 10 == 1:
            galaxies[i, 3:6] = np.array([1.0, 1.0, 1.0], dtype=np.float32) * brightness  # White
        elif i % 10 == 2 or i % 10 == 3 or i % 10 == 4:
            galaxies[i, 3:6] = np.array([0.5, 0.5, 0.5], dtype=np.float32) * brightness  # Gray
        elif i % 10 == 5:
            galaxies[i, 3:6] = np.array([0.98, 0.0, 0.603], dtype=np.float32) * brightness  # Pink
        elif i % 10 == 6:
            galaxies[i, 3:6] = np.array([0.54, 0.81, 0.94], dtype=np.float32) * brightness  # Baby blue

    return galaxies

def create_vbo(galaxies):
    vbo_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferData(GL_ARRAY_BUFFER, galaxies.nbytes, galaxies, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo_id

def draw_galaxies(vbo_id, num_galaxies):
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, None)  # Update stride to 24 bytes (6 floats)
    glColorPointer(3, GL_FLOAT, 24, ctypes.c_void_p(12))  # Set the color pointer offset to 12 bytes (3 floats)

    glPointSize(1.0)  # Adjust the point size for better visibility of galaxies

    # Add alpha blending for a more visually appealing effect
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Enable depth testing to correctly render the web effect
    glEnable(GL_DEPTH_TEST)

    glDrawArrays(GL_POINTS, 0, num_galaxies)

    # Disable point sprite rendering and depth testing
    glDisable(GL_POINT_SPRITE)
    glDisable(GL_DEPTH_TEST)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def main(num_galaxies):
    init()
    galaxies = generate_galaxies(num_galaxies)
    vbo_id = create_vbo(galaxies)

    clock = pygame.time.Clock()
    fps_counter = 0
    start_time = time.time()
    fullscreen_toggle = False  # Flag to track fullscreen toggle

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not fullscreen_toggle:
                        pygame.display.toggle_fullscreen()
                        fullscreen_toggle = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    fullscreen_toggle = False

        glRotatef(0.1, 0.1, 0.1, 0.1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_galaxies(vbo_id, num_galaxies)
        pygame.display.flip()

        fps_counter += 1
        if time.time() - start_time >= 1.0:
            print("FPS:", fps_counter)
            fps_counter = 0
            start_time = time.time()

        clock.tick(60)  # Limit frame rate to 60 FPS

if __name__ == '__main__':
    num_galaxies = 200000  # Set the number of galaxies here
    main(num_galaxies)
