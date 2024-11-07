import random

class Drone:
    def __init__(self, pygame, screen, position, speed, direction, radius=0):
        self.pygame = pygame
        self.screen = screen
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.direction = pygame.Vector2(direction).normalize()
        self.radius = radius
        
        # Scale the image if necessary
        # self.image = self.pygame.image.load('./drone/red-drone.webp')
        # self.image = self.pygame.transform.scale(self.image, (5, 5)) 

        self.id = random.randint(0, 10000)

        # print("Drone created with id: ", self.id)
    
    def update(self):
        # print("Updating drone with id: ", self.id)
        self.position += self.direction * self.speed

    def set_direction(self, direction):
        if direction[0] == 0 and direction[1] == 0:
            self.pygame.Vector2(direction)
            return

        self.direction = self.pygame.Vector2(direction).normalize()

    def set_direction_by_coords(self, coords):
        self.set_direction((coords[0] - self.position.x, coords[1] - self.position.y))

    def draw(self):
        # Draw the drone image
        # self.screen.blit(self.image, (int(self.position.x), int(self.position.y)))
        # print("Drawing drone with id: ", self.id)
        self.pygame.draw.circle(self.screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), 3)