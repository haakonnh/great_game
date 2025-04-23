import pymunk
from pymunk.vec2d import Vec2d

class GameObject:
    def __init__(self, position, mass=1, radius=10):
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = Vec2d(position[0], position[1])
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5

    def add_to_space(self, space):
        space.add(self.body, self.shape)
