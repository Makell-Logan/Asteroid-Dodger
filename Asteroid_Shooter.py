import pygame
import sys
import random

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.shield_surface = pygame.image.load("Meteor Dodger Assets/shield.png")
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos() # Gets the position of mouse
        self.screen_constrain()
        self.display_health()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0

    def display_health(self):
        for index,shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10 + index *40,10))

    def get_damage(self,damage_amount):
        self.health -= damage_amount

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
        if self.rect.centery >= 800:
            self.kill() # This despawns the sprite once it leaves the screen

class Laser(pygame.sprite.Sprite):
        def __init__(self,path,pos,speed):
            super().__init__()
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(center = (pos))
            self.speed = speed
        
        def update(self):
            self.rect.centery -= self.speed
            if self.rect.centery <= -100:
                self.kill()


pygame.init() # initiate pygame
screen = pygame.display.set_mode((1280,720)) # Create display surface
clock = pygame.time.Clock() # Create clock object

spaceship = SpaceShip("Meteor Dodger Assets/spaceship.png",640,500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT,100) # This event triggers every 100 miliseconds

laser_group = pygame.sprite.Group()

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            new_laser = Laser("Meteor Dodger Assets/Laser.png",event.pos,15)
            laser_group.add(new_laser)

    screen.fill((42,45,51))
    
    laser_group.draw(screen)
    spaceship_group.draw(screen) # Adds the spacesship_group object to the screen
    meteor_group.draw(screen) # Adds the meteor_group object to the screen
    

    laser_group.update()
    spaceship_group.update()
    meteor_group.update()

    if pygame.sprite.spritecollide(spaceship_group.sprite,meteor_group,True): # Detects if the sprite in spaceship_group has collided with any sprite in meteor_group, if so since the third parameter is true despawn the sprite it collided with
        spaceship_group.sprite.get_damage(1)

    for laser in laser_group:
        pygame.sprite.spritecollide(laser,meteor_group,True)

    pygame.display.update() # Draw frame
    clock.tick(120) # Control the framerate