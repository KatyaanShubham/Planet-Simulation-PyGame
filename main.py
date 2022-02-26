import pygame
import math


pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Of Planets")

White = (255, 255, 255)
Orange = (255,165,0)
Blue = (55, 145, 223)
Red = (210, 27, 10)
Grey = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11 
    SCALE = 250/AU          #1AU = 100 pixels
    Timestep = 3600 * 24    # 1 day
    

    def __init__(self, x, y, color, mass, radius):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.radius = radius

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE+ width/2
        y = self.y * self.SCALE + height/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + width/2
                y = y * self.SCALE + height/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km",1, White)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))


    def frc_attr(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.frc_attr(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.Timestep
        self.y_vel += total_fy / self.mass * self.Timestep

        self.x += self.x_vel * self.Timestep
        self.y += self.y_vel * self.Timestep
        self.orbit.append((self.x, self.y))




def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, Orange, 1.98892 * 10**30, 30)
    sun.sun = True

    Earth = Planet(-1 * Planet.AU, 0, Blue, 5.9742* 10**24, 22)
    Earth.y_vel = 29.783 * 1000

    Mercury = Planet(0.387 * Planet.AU, 0, Grey, 3.30* 10**23, 10)
    Mercury.y_vel = -47.4 * 1000

    Venus = Planet(0.723 * Planet.AU, 0, White, 4.8685* 10**24, 14)
    Venus.y_vel = -35.02 * 1000

    Mars = Planet(-1.524 * Planet.AU, 0, Red, 6.39* 10**23, 18)
    Mars.y_vel = 24.077 * 1000

    planets = [sun, Mercury, Venus, Earth, Mars]

    while run:
        clock.tick(60)
        screen.fill((0, 0, 0))
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets )
            planet.draw(screen)

        pygame.display.update()

    pygame.quit()       

main()
