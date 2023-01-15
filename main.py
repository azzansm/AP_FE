import pygame
import os
import random
import sys

pygame.init()

# global constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# to add pictures we will be using pygame.image.load(os.path.join())
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80  # x position of the dinosaur on the screen
    Y_POS = 310  # y position of  the dinosaur on the screen
    Y_POS_DUCK = 340  # when ducking, the dinosaur need to be shown further down the screen
    JUMP_VEL = 8.5  # velocity of the dinosaur as soon as it jumps

    def __init__(self):  # to initialize the dinosaur whenever an object of this class is created
        # innit method is used to include all the images of the dinosaur
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True  # the dinosaur neither ducking nor jumping, it's simply running on the road
        self.dino_jump = False

        self.step_index = 0  # to animate the dinosaur
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]  # initialize the first image
        # to get the rectangle of the dinosaur image:
        self.dino_rect = self.image.get_rect()  # which is going to be the hit boxes for the dinosaur later on
        self.dino_rect.x = self.X_POS  # the x coordinate for the rectangle
        self.dino_rect.y = self.Y_POS  # the y coordinate for the rectangle

    #  updates the dinosaur every while loop iteration
    def update(self, userInput):  # as an argument the update function is going to get the user input
        if self.dino_duck:  # a corresponding function is called depending on the dinosaur
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:  # reset every ten steps as it will help to animate the dinosaur further down the line
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True  # up on the keyboard is used to jump
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True  # down on the keyboard is used to duck
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True  # other than that, it will be used for the dinosaur to run
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK  # the position of dinosaur ducking will be displayed
        self.step_index += 1

    def run(self):
        # self.step_index helps rotate through the individual images in order to make it look like its being animated
        self.image = self.run_img[self.step_index // 5]  # set to the corresponding image of the dinosaur running
        self.dino_rect = self.image.get_rect()  # rectangle coordinates of the image
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        # when the step index in between value of 0 and 5, the first image will be displayed
        # when the step index between the value of 5 and 10, the second image will be displayed
        self.step_index += 1
        # and beyond the value of 10, the step index is reset, hence the images will be displayed sequentially
        # making the dinosaur look animated

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:  # if the state of the dinosaur is set to jumping
            self.dino_rect.y -= self.jump_vel * 4  # decreasing the y position, so it moves up on the screen
            self.jump_vel -= 0.8  # decreasing the velocity
        if self.jump_vel < - self.JUMP_VEL:  # the state as soon as the vel of dinosaur reaches 8.5
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):  # screen as an argument
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))  # used to blitz the image onto the screen


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # used to specify the coordinates of the cloud
        self.y = random.randint(50, 100)
        self.y = random.randint(50, 100)

        self.image = CLOUD  # to attach the cloud image
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:  # to make the cloud appears again whenever the cloud moves off the screen
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))  # blitz the image onto the screen


class Obstacle:
    def __init__(self, image, type):
        self.image = image  # image of the obstacles
        self.type = type  # the type of the obstacles in integer value
        self.rect = self.image[self.type].get_rect()  # rect coordinates of the img
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:  # moves the obstacles off the screen on the left hand side
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)  # blit the image onto the screen


class SmallCactus(Obstacle):  # inherit from the class obstacle
    def __init__(self, image):  # take the img as parameter
        self.type = random.randint(0, 2)  # set the type of the cactus
        super().__init__(image, self.type)  # initialize with the parent class
        self.rect.y = 325  # set the coordinates


class LargeCactus(Obstacle):  # identical with the class small cactus
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300  # except, the coordinate will be lower


class Bird(Obstacle):  # inherit from class obstacle
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)  # initialize with the parent class
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):  # overrides the parent class
        if self.index >= 9:  # reset the index to the initial value once it reaches the value of 9
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        # when the index in between value of 0 and 5, the first image will be displayed
        # when the index between the value of 5 and 10, the second image will be displayed
        self.index += 1
        # and beyond the value of 10, the index is reset, hence the images will be displayed sequentially
        # making the bird look animated


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    # global var obstacles is going to store all the obstacles such as the bird and cactus
    run = True  # give a switch
    clock = pygame.time.Clock()  # to time the game
    player = Dinosaur()  # an instance of the class dinosaur
    cloud = Cloud()
    game_speed = 20  # keep track at how fast everything on the screen is moving
    x_pos_bg = 0  # initial value of x coordinate of the bg
    y_pos_bg = 380  # initial value of y coordinate of the bg
    points = 0  # the initial points of the game
    font = pygame.font.SysFont('georgia', 30)  # used to display the score
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed  # global variable
        points += 1  # every single time the function is called, it will increment the var points by one
        if points % 100 == 0:  # check whenever the points is a multiple of 100
            game_speed += 1  # the speed will be incremented by one everytime the user reaches 100 or multiple of 100

        text = font.render("Points: " + str(points), True, (255, 255, 255))  # display the points
        textRect = text.get_rect()  # rectangle of where the points will be displayed
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)  # blitz the screen

    def background():
        global x_pos_bg, y_pos_bg  # global coordinate
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:  # whenever one bg image moves off the screen, another one is created right after
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed  # from the x pos of the bg, it will subtract the game speed

    while run:  # to close the game whenever user clicks the small X on the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((0, 0, 0))  # bg color
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)  # draw the dinosaur onto the screen
        player.update(userInput)  # update the dinosaur on every while loop iteration

        if len(obstacles) == 0:  # if the length of obstacle is zero, it will randomly create
            # either small cactus, large cactus, or bird
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:  # call the functions
            obstacle.draw(SCREEN)
            obstacle.update()
            # if statement for the collision detection
            # if the rect of the dinosaur img collides with the rect of the obstacles
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)  # to see how the dino died
                death_count += 1  # increment the death count
                menu(death_count)

        background()  # call function to run the game

        cloud.draw(SCREEN)  # call the function cloud
        cloud.update()  # to update the display

        score()

        clock.tick(30)  # timing of the game
        pygame.display.update()  # to update the display


def menu(death_count):
    global points  # to display the points when the game ends
    run = True
    while run:
        SCREEN.fill((0, 0, 0))  # black bg
        font = pygame.font.SysFont('georgia', 50)  # fonts

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (255, 255, 255))
        elif death_count > 0:  # when the death count is greater than 0, display the option to restart
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Your Score: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()  # position of the texts
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # display of the dinosaur running
        pygame.display.update()  # update the display
        for event in pygame.event.get():  # option to quit the game safely
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()  # runs the main function


menu(death_count=0)  # called the menu function and set the death count to zero
