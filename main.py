import pygame as pg
import moderngl as mgl
import struct
import sys

class App:
    def __init__(self, win_size=(2560, 1440)):
        #OpenGL Context
        pg.display.set_mode(win_size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        self.ctx = mgl.create_context()

        #Time Objects
        self.clock = pg.time.Clock()

        #Load Shaders
        with open('programs/vertex.glsl') as f:
            vertex = f.read()
        with open ('programs/fragment.glsl') as f:
            fragment = f.read()
        self.program = self.ctx.program(vertex_shader=vertex, fragment_shader=fragment)

        #Quad Screen Vertices
        vertices = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1), (1, 1)]

        #Quad VBO
        vertex_data = struct.pack(f'{len(vertices) * len(vertices[0])}f', *sum(vertices, ()))
        self.vbo = self.ctx.buffer(vertex_data)

        #Quad VAO
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '2f', 'in_position')])

        #Uniforms
        self.set_uniform('u_resolution', win_size)

    def render(self):
        self.ctx.clear()
        self.vao.render()
        pg.display.flip()

    def update(self):
        self.set_uniform('u_time', pg.time.get_ticks() * 0.001)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.render()
            self.clock.tick(0)

    def set_uniform(self, u_name, u_value):
        try:
            self.program[u_name] = u_value
        except KeyError:
            pass

    def destroy(self):
        self.vbo.release()
        self.program.release()
        self.vao.release()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()