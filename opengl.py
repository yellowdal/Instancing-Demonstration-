import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

vertex_src = """
# version 330
layout(location=0)in vec3 a_position;

uniform mat4 rotation;

void main()
{
    gl_Position =  rotation * vec4(a_position, 1.0);
   
}
"""

fragment_src = """
# version 330

out vec4 out_color;
void main()
{
    out_color = vec4(0.0,0.0,1.0, 1.0);
}
"""


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# initialising the glfw library

if not glfw.init():
    raise Exception("glfw cannot be initialised")

# Creating The OpenGL(glfw) window [first step]
window = glfw.create_window(1200, 750, 'opengl', None, None)

# for checking window is created or not
if not window:
    glfw.terminate()
    raise Exception("Window cannot be created")

# setting windows postion thats where display of window will begin
glfw.set_window_pos(window, 400, 200)

glfw.set_window_size_callback(window, window_resize)

# making context current
glfw.make_context_current(window)
# For Triangle vertices
'''vertices = [-0.5, -0.5, 0.0,  # Bottom left corner
            0.5, -0.5, 0.0,  # Bottom right corner
            0.0, 0.5, 0.0  # Top center pointer
            ]'''

vertices = [-0.5, -0.5, 0.5,
            0.5, -0.5, 0.5,
            0.5, 0.5, 0.5,
            -0.5, 0.5, 0.5,

            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, 0.5, -0.5,
            -0.5, 0.5, -0.5,
            ]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]
vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Element BufferObject
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# position = glGetAttribLocation(shader, "a_position")


glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, 24, GL_FALSE, ctypes.c_void_p(0))

glUseProgram(shader)

# this where window will get displayed

rotation_loc = glGetUniformLocation(shader, "rotation")

glEnable(GL_DEPTH_TEST)
while not glfw.window_should_close(window):
    glfw.poll_events()
    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glClear(GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time())

    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x * rot_y)

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

glfw.terminate()
