'''
Title: Double Pendulum
Author: SammygoodTunes
Version: 1.1
'''

import math
import pygame
import random as r

pygame.init()


class Window:
    def __init__(self):
        self.width, self.height = 512, 512
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption("Double Pendulum")
        self.clock = pygame.time.Clock()

    def get_size(self):
        return self.width, self.height


class Simulation:
    def __init__(self):
        self.path_surface = pygame.Surface((0, 0))
        self.end = False
        self.px, self.py = 0, 0
        self.p1_x, self.p1_y = 0, 0
        self.p2_x, self.p2_y = 0, 0
        self.p1_length, self.p2_length = 125, 125
        self.p1_mass, self.p2_mass = 10, 10
        self.p1_angle, self.p2_angle = r.randint(-16, 16) + math.pi/r.uniform(1, 8), r.randint(-16, 16) + math.pi/r.uniform(1, 8)
        self.p1_velocity, self.p2_velocity = 0, 0
        self.p1_acceleration, self.p2_acceleration = 0, 0
        self.prev = [self.px, self.py, self.p1_x, self.p1_y, self.p2_x, self.p2_y]

    def set_path_surface(self, window):
        self.path_surface = pygame.Surface(window.get_size())

    def pendulum1(self, window):
        self.px, self.py = window.get_size()[0] / 2, 256
        self.p1_x = self.p1_length * math.sin(self.p1_angle)
        self.p1_y = self.p1_length * math.cos(self.p1_angle)
        return self.px, self.py, self.p1_x, self.p1_y

    def pendulum2(self):
        self.p2_x = self.p2_length * math.sin(self.p2_angle)
        self.p2_y = self.p2_length * math.cos(self.p2_angle)
        return self.p2_x, self.p2_y

    def stop(self):
        self.end = True


def main():
    window = Window()
    sim = Simulation()
    sim.set_path_surface(window)
    while not sim.end:
        window.screen.fill((0, 0, 0), (0, 0, window.get_size()[0], window.get_size()[1]))
        window.screen.blit(sim.path_surface, (0, 0))
        px, py, p1_x, p1_y = sim.pendulum1(window)
        p2_x, p2_y = sim.pendulum2()
        if sim.prev[0] != 0:
            pygame.draw.line(sim.path_surface, (255, 0, 0),
                             (sim.prev[0] + sim.prev[2] + sim.prev[4], sim.prev[1] + sim.prev[3] + sim.prev[5]),
                             (px + p1_x + p2_x, py + p1_y + p2_y))
        sim.prev = [px, py, p1_x, p1_y, p2_x, p2_y]
        pygame.draw.line(window.screen, (255, 255, 255), (px, py), (px + p1_x, py + p1_y))
        pygame.draw.line(window.screen, (255, 255, 255), (px + p1_x, py + p1_y), (px + p1_x + p2_x, py + p1_y + p2_y))
        pygame.draw.ellipse(window.screen, (255, 255, 255),
                            [px + p1_x - sim.p1_mass / 2 + 1, py + p1_y - sim.p1_mass / 2 + 1,
                             sim.p1_mass, sim.p1_mass])
        pygame.draw.ellipse(window.screen, (255, 255, 255),
                            [px + p1_x + p2_x - sim.p2_mass / 2 + 1, py + p1_y + p2_y - sim.p2_mass / 2 + 1,
                             sim.p2_mass, sim.p2_mass])

        g = 0.9806

        n1 = -g * (2 * sim.p1_mass + sim.p2_mass) * math.sin(sim.p1_angle)
        n2 = -sim.p2_mass * g * math.sin(sim.p1_angle - 2 * sim.p2_angle)
        n3 = -2 * math.sin(sim.p1_angle - sim.p2_angle) * sim.p2_mass
        n4 = sim.p2_velocity ** 2 * sim.p2_length + sim.p1_velocity**2 * sim.p1_length * math.cos(sim.p1_angle - sim.p2_angle)
        n5 = sim.p1_length * (2 * sim.p1_mass + sim.p2_mass - sim.p2_mass * math.cos(2 * sim.p1_angle - 2 * sim.p2_angle))
        sim.p1_acceleration = (n1 + n2 + n3 * n4) / n5

        n1 = 2 * math.sin(sim.p1_angle - sim.p2_angle)
        n2 = sim.p1_velocity ** 2 * sim.p1_length * (sim.p1_mass + sim.p2_mass)
        n3 = g * (sim.p1_mass + sim.p2_mass) * math.cos(sim.p1_angle)
        n4 = sim.p2_velocity ** 2 * sim.p2_length * sim.p2_mass * math.cos(sim.p1_angle - sim.p2_angle)
        n5 = sim.p2_length * (2 * sim.p1_mass + sim.p2_mass - sim.p2_mass * math.cos(2 * sim.p1_angle - 2 * sim.p2_angle))
        sim.p2_acceleration = (n1 * (n2 + n3 + n4)) / n5

        print("acc:", sim.p1_acceleration, sim.p2_acceleration)
        print("vel:", sim.p1_velocity, sim.p2_velocity)
        print("ang:", sim.p1_angle, sim.p2_angle)

        sim.p1_velocity += sim.p1_acceleration
        sim.p2_velocity += sim.p2_acceleration
        sim.p1_angle += sim.p1_velocity
        sim.p2_angle += sim.p2_velocity

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sim.stop()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sim.path_surface.fill((0, 0, 0), (0, 0, window.get_size()[0], window.get_size()[1]))
                    window = Window()
                    sim = Simulation()
                    sim.set_path_surface(window)



        window.clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
