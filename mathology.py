import pygame
import random
import operator
from pygame.locals import *

pygame.font.init()

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
RED       = (255,   0,   0)
BLUE      = (  0,   0, 255)
GREEN     = (  0, 255,   0)
# ---- Static variables -----
OPERATORS = [operator.add, operator.sub, operator.truediv, operator.mul]
# screen size
display_width = 800
display_height = 600


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Mathology')
clock = pygame.time.Clock()


class GameButton:

    def __init__(self, value, coord_list):
        self.value = value
        self.x = coord_list[0]
        self.y = coord_list[1]
        self.width = coord_list[2]
        self.height = coord_list[3]
        self.color = GRAY
        self.mouse_over = False
        self.mouse_down = False
        self.clicked = False
        self.operated = False

    def handle_event(self, events):
        if self.clicked is False:
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_over_button(event.pos)

                if self.mouse_over:
                    self.color = WHITE
                else:
                    self.color = GRAY

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.mouse_over:
                        self.mouse_down = True
                    else:
                        self.mouse_down = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mouse_down and self.mouse_over:
                        print('clicked:', self.value)
                        self.clicked = True

    def mouse_over_button(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.mouse_over = True
        else:
            self.mouse_over = False

    def button_text(self):
        small_text = pygame.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.text_objects(small_text)
        text_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        gameDisplay.blit(text_surf, text_rect)

    def text_objects(self, font):
        text_surface = font.render(self.value, True, RED)
        return text_surface, text_surface.get_rect()

    def draw_button(self):
        if self.clicked is False:
            pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height))
            self.button_text()
        else:
            pygame.draw.rect(gameDisplay, RED, (self.x, self.y, self.width, self.height))


class ResetButton:

    def __init__(self, reset):  # reset is the GoalField.start Value
        self.clicked = False
        self.counter = 0
        self.goal_value = reset
        self.color = GRAY
        self.x = 450
        self.y = 100
        self.width = 100
        self.height = 50
        self.mouse_over = False
        self.mouse_down = False

    def mouse_over_button(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.mouse_over = True
        else:
            self.mouse_over = False

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_over_button(event.pos)

            if self.mouse_over:
                self.color = WHITE
            else:
                self.color = GRAY

    def draw_button(self):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height))
        self.button_text()

    def button_text(self):
        small_text = pygame.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.text_objects(small_text)
        text_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        gameDisplay.blit(text_surf, text_rect)

    def text_objects(self, font):
        text_surface = font.render('Reset: '+str(self.counter), True, RED)
        return text_surface, text_surface.get_rect()


class GoalField:

    def __init__(self, value):
        self.start = value
        self.value = value
        self.x = 10
        self.y = 10
        self.width = display_width - 20
        self.height = 50
        self.win = False

    def operate(self, button, operator):
        if button.operated is False:
            if operator == "-":
                self.value = int(self.value) - int(button.value)
                button.operated = True
            if operator == "+":
                self.value = int(self.value) + int(button.value)
                button.operated = True
            if operator == "/":
                self.value = int(self.value) / int(button.value)
                button.operated = True
            if operator == "*":
                self.value = int(self.value) * int(button.value)
                button.operated = True
        else:
            pass

        if int(self.value) == 0:
            self.win = True

    def button_text(self):
        small_text = pygame.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.text_objects(small_text)
        text_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        gameDisplay.blit(text_surf, text_rect)

    def text_objects(self, font):
        text_surface = font.render(str(self.value), True, RED)
        return text_surface, text_surface.get_rect()

    def draw_field(self):
        pygame.draw.rect(gameDisplay, WHITE, (self.x, self.y, self.width, self.height))
        self.button_text()

def button_grid():
    space = 10
    size = 100
    row_1 = 100
    row_2 = row_1 + 110
    row_3 = row_2 + 110
    locations = []

    for i in range(0, 4):
        push = (space + size) * i
        locations.append([space + push, row_1, size, size])
        locations.append([space + push, row_2, size, size])
        locations.append([space + push, row_3, size, size])

    return locations

def create_goal():
    first_random = random.randrange(1, 30)
    goal_list = [first_random]
    for i in range(3, 5):
        number = random.randrange(1, 30)
        goal_list.append(number)
    random.shuffle(goal_list)
    return goal_list

def game_loop():
    goal_list = create_goal()
    goal = GoalField(str(sum(goal_list)))
    reset = ResetButton(str(goal.start))
    grid = button_grid()
    buttons = []
    for i in range(len(goal_list), 12):
        goal_list.append(random.randrange(1, 30))
    for i in range(12):
        buttons.append(GameButton(str(goal_list[i]), grid[i]))

    counter = 1

    playing = True
    while playing:

        gameDisplay.fill(BLACK)
        for button in buttons:
            button.draw_button()
        events = pygame.event.get()
        for button in buttons:
            button.handle_event(events)
            if button.clicked is True:
                goal.operate(button, '-')
        reset.handle_event(events)
        goal.draw_field()
        reset.draw_button()


        if goal.win is True:
            large_text = pygame.font.Font('freesansbold.ttf', random.randrange(50, 100))
            text_surf = large_text.render('YOU WIN', True, BLUE)
            text_rect = text_surf.get_rect()
            text_rect.center = ((display_width / 2), (display_height / 2))
            gameDisplay.blit(text_surf, text_rect)
            counter += 1
        if counter > 50:
            game_loop()
        pygame.display.update()

        if int(goal.value) < 0:
            game_loop()


        for event in events:
            if event.type == pygame.QUIT:
                playing = False

        clock.tick(10)

    pygame.quit()
    quit()


game_loop()
