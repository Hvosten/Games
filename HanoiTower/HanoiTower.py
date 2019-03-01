import pygame
import sys
import random

from pygame.locals import *

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
pink = (255, 0, 255)
orange = (204, 102, 0)
mint = (0, 204, 153)

colors = [red, green, yellow, white, pink, orange, mint, black, (127, 0, 255), (0, 102, 102), (255, 0, 127),
          (0, 102, 204), (96, 96, 96), (153, 153, 0)]

pygame.init()


class Element:
    moves = 0

    def __init__(self, w, h, x, y, c):
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.color = c
        self.rectangle = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.rectangle_dragging = False

        self.offset_x = 0
        self.offset_y = 0

    def move_element(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rectangle.collidepoint(event.pos):
                    self.rectangle_dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rectangle.x - mouse_x
                    self.offset_y = self.rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.rectangle_dragging = False
                if (self.rectangle.x < 300 < self.rectangle.x + self.width) or \
                        (self.rectangle.x < 600 < self.rectangle.x + self.width) or \
                        (self.rectangle.y < 160 or self.rectangle.y + self.height < 160):
                    self.rectangle.x = self.x
                    self.rectangle.y = self.y
                elif self.rectangle.x < 300:
                    return 0
                elif self.rectangle.x < 600:
                    return 1
                else:
                    return 2

        elif event.type == pygame.MOUSEMOTION:
            if self.rectangle_dragging:
                mouse_x, mouse_y = event.pos
                self.rectangle.x = mouse_x + self.offset_x
                self.rectangle.y = mouse_y + self.offset_y

    def show_element(self, screen):
        pygame.draw.rect(screen, self.color, self.rectangle)

    def restore_position(self):
        self.rectangle.x = self.x
        self.rectangle.y = self.y

    def place_element(self, num_of_el, num_of_stack):
        self.x = 300*num_of_stack + (150 - self.width/2)
        self.y = 460 - 40*num_of_el
        self.restore_position()
        Element.moves += 1


class Game:

    def __init__(self):
        self.width = 900
        self.length = 540
        self.screen = pygame.display.set_mode((self.width, self.length))
        pygame.display.set_caption('Hanoi Tower')

        self.num_of_elem = 4
        self.increase_decrease = pygame.Rect(110, 105, 50, 30)
        self.solve = pygame.Rect(100, 510, 100, 30)

        self.stack = [[], [], []]

        self.new_game()

        self.steps_to_solve = []

        while True:
            for event in pygame.event.get():
                self.actions(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.increase_decrease.collidepoint(event.pos):
                        if event.button == 1 and self.num_of_elem < 8:  # Left button.
                            self.num_of_elem += 1
                            self.new_game()
                        elif event.button == 3 and self.num_of_elem > 4:  # Right button.
                            self.num_of_elem -= 1
                            self.new_game()
                    if self.solve.collidepoint(event.pos):
                        self.solve_it()

                if len(self.stack[0]) > 0:
                    position = self.stack[0][-1].move_element(event)
                    if isinstance(position, int):
                        self.move_element(0, position)

                if len(self.stack[1]) > 0:
                    position = self.stack[1][-1].move_element(event)
                    if isinstance(position, int):
                        self.move_element(1, position)

                if len(self.stack[2]) > 0:
                    position = self.stack[2][-1].move_element(event)
                    if isinstance(position, int):
                        self.move_element(2, position)

                self.draw()

    def actions(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit(0)

    def new_game(self):
        self.stack[0].clear()
        self.stack[1].clear()
        self.stack[2].clear()
        Element.moves = 0
        the_chosen_ones = random.sample(colors, self.num_of_elem)
        for i in range(0, self.num_of_elem):
            self.stack[0].append(Element(240-30*i, 40, 30+15*i, 460-40*i, the_chosen_ones[i]))

    def move_element(self, previous_p, new_p):
        if previous_p == new_p or (len(self.stack[new_p]) > 0 and
                                   self.stack[previous_p][-1].width > self.stack[new_p][-1].width):
            self.stack[previous_p][-1].restore_position()
        else:
            self.stack[new_p].append(self.stack[previous_p][-1])
            self.stack[previous_p].pop()
            self.stack[new_p][-1].place_element(len(self.stack[new_p])-1, new_p)

    def draw(self):
        surf = pygame.Surface((300, 380))
        surf.fill((204, 255, 153))
        self.screen.blit(surf, (0, 160))

        surf.fill((255, 153, 255))
        self.screen.blit(surf, (300, 160))

        surf.fill((153, 204, 255))
        self.screen.blit(surf, (600, 160))

        surf2 = pygame.Surface((900, 160))
        surf2.fill((255, 153, 153))
        self.screen.blit(surf2, (0, 0))

        myfont = pygame.font.SysFont("arialblack", 40)
        text = myfont.render("TOWER OF HANOI", True, (0, 128, 255))
        self.screen.blit(text, (255, 30))

        myfont = pygame.font.SysFont("arialblack", 20)
        text = myfont.render("Minimum moves: {}".format(2 ** self.num_of_elem - 1), True, (204, 0, 51))
        self.screen.blit(text, (340, 130))

        myfont = pygame.font.SysFont("arialblack", 20)
        text = myfont.render("Moves: {}".format(Element.moves), True, (204, 0, 51))
        self.screen.blit(text, (700, 130))

        myfont = pygame.font.SysFont("arialblack", 20)
        text = myfont.render("Destination", True, (204, 0, 51))
        self.screen.blit(text, (690, 510))

        pygame.draw.rect(self.screen, (34, 139, 34), self.increase_decrease)
        font = pygame.font.Font(None, 40)
        txt = font.render(str(self.num_of_elem), True, (34, 139, 34))
        self.screen.blit(txt, (170, 105))

        pygame.draw.rect(self.screen, (255, 215, 0), self.solve)
        font = pygame.font.SysFont("arialblack", 20)
        txt = font.render("SOLVE", True, (255, 69, 0))
        self.screen.blit(txt, (115, 510))

        myfont = pygame.font.SysFont("arialblack", 15)
        text = myfont.render("Increase/Decrease number of discs", True, (34, 139, 34))
        self.screen.blit(text, (5, 135))

        if len(self.stack[2]) == self.num_of_elem:
            myfont = pygame.font.SysFont("arialblack", 25)
            text = myfont.render("YOU DID IT!", True, (0, 128, 0))
            self.screen.blit(text, (370, 350))

        for e in self.stack[0]:
            e.show_element(self.screen)
        for e in self.stack[1]:
            e.show_element(self.screen)
        for e in self.stack[2]:
            e.show_element(self.screen)
        pygame.display.flip()

    def generate_steps(self, n, a, b, c):
        if n == 1:
            self.steps_to_solve.append((a, c))
        else:
            self.generate_steps(n-1, a, c, b)
            self.generate_steps(1, a, b, c)
            self.generate_steps(n-1, b, a, c)

    def solve_it(self):
        self.new_game()
        self.generate_steps(self.num_of_elem, 0, 1, 2)
        for move in self.steps_to_solve:
            for event in pygame.event.get():
                self.actions(event)
            self.draw()
            self.move_element(move[0], move[1])
            pygame.time.wait(1000)


if __name__ == '__main__':
    Game()
