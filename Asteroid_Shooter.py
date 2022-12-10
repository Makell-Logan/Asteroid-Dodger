import pygame
import sys
import random

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

    def update(self):
        self.rect.center = pygame.mouse.get_pos() # Gets the position of mouse
        self.screen_constrain()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0

class Meteor(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos,x_speed,y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        if self.rect.center >= 800:
            self.kill() # This despawns the sprite once it leaves the screen

class Laser(pygame.sprite.Sprite):
        def __init__(self,path,x_pos,y_pos,speed):
            super().__init__()
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(center = (x_pos,y_pos))



pygame.init() # initiate pygame
screen = pygame.display.set_mode((1280,720)) # Create display surface
clock = pygame.time.Clock() # Create clock object

spaceship = SpaceShip("Meteor Dodger Assets/spaceship.png",640,500,10)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor_group = pygame.sprite.Group()

METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT,100) # This event triggers every 100 miliseconds

while True: # Game loop
    for event in pygame.event.get(): # Check for events / Player input
        if event.type == pygame.QUIT: # Close the game
            pygame.quit()
            sys.exit()
        if event.type == METEOR_EVENT:
            meteor_path = random.choice(("Meteor Dodger Assets/Meteor1.png", "Meteor Dodger Assets/Meteor2.png", "Meteor Dodger Assets/Meteor3.png"))
            random_x_pos = random.randrange(0,1280)
            random_y_pos = random.randrange(-500,-50)
            random_x_speed = random.randrange (-1,1)
            random_y_speed = random.randrange (4,10)
            meteor = Meteor(meteor_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
            meteor_group.add(meteor)

    screen.fill((42,45,51))
    spaceship_group.draw(screen) # Adds the object to the screen
    spaceship_group.update()
    
    meteor_group.draw(screen) # Adds the object to the screen
    meteor_group.update()

    pygame.display.update() # Draw frame
    clock.tick(120) # Control the framerate