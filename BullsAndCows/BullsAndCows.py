import pygame
import sys
from random import randint

from pygame.locals import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

background = (255, 170, 29)
interior = (127, 255, 212)
color_win = (0, 128, 0)
color_title = (255, 32, 82)
color_tips = (61, 12, 2)


class Game:

    def __init__(self):
        self.to_guess = str(randint(1000, 9999))
        self.attempts = 0
        self.previous_attempts = {}

        self.width = 900
        self.length = 640
        self.screen = pygame.display.set_mode((self.width, self.length))
        self.screen.fill(white)
        pygame.display.set_caption('Bulls&Cows Game')

        self.bullImg = pygame.image.load('bull.png')
        self.cowImg = pygame.image.load('cow.png')

        self.guess = ''
        self.input_box = pygame.Rect(440, 230, 70, 32)

        self.win = False
        self.wrong_input = False

        while True:
            self.screen.fill(background)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.win:
                        self.new_game()
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    if event.key == pygame.K_RETURN:
                        self.wrong_input = False
                        self.check_the_guess()
                        self.guess = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.guess = self.guess[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif not self.win:
                        self.guess += event.unicode

            self.draw()
            self.write_guesses()
            if self.win:
                self.after_win()
            pygame.display.flip()

    @staticmethod
    def split_into_digits(s):
        digits = []
        for c in s:
            digits.append(c)
        return digits

    def how_many_bulls(self, user_guess):
        counter = 0
        for i in range(len(self.to_guess)):
            if self.to_guess[i] == user_guess[i]:
                counter += 1
        return counter

    def how_many_bulls_and_cows(self, user_guess):
        counter = 0
        list1 = self.split_into_digits(self.to_guess)
        list2 = self.split_into_digits(user_guess)

        for e in list1:
            if e in list2:
                list2.remove(e)
                counter = counter + 1
        return counter

    def new_game(self):
        self.to_guess = str(randint(1000, 9999))
        self.attempts = 0
        self.previous_attempts = {}
        self.win = False

    def check_the_guess(self):
        try:
            val = int(self.guess)
        except ValueError:
            self.wrong_input = True
            return
        if len(self.guess) != 4 or len(str(val)) != 4:
            self.wrong_input = True
            return
        self.attempts += 1
        bulls = self.how_many_bulls(self.guess)
        cows = self.how_many_bulls_and_cows(self.guess) - bulls
        self.previous_attempts[self.attempts] = (self.guess, bulls, cows)
        if bulls == 4:
            self.win = True

    def draw(self):
        font = pygame.font.Font(None, 32)
        title = pygame.Surface((self.width, 100))
        title.fill(interior)
        self.screen.blit(title, (0, 40))

        surf = pygame.Surface((300, 200))
        surf.fill((251, 206, 177))
        self.screen.blit(surf, (330, 200))

        myfont = pygame.font.SysFont("comicsansms", 80)
        text = myfont.render("Bulls&Cows", 1, color_title)
        self.screen.blit(text, (270, 30))

        myfont = pygame.font.SysFont("candara", 30)
        text2 = myfont.render("Guess 4-digits number:", 1, color_tips)
        self.screen.blit(text2, (330, 200))

        myfont = pygame.font.SysFont("candara", 19)
        text2 = myfont.render("Bull(B) - number of matched digits in ", 1, color_tips)
        self.screen.blit(text2, (330, 300))

        myfont = pygame.font.SysFont("candara", 19)
        text2 = myfont.render("right positions", 1, color_tips)
        self.screen.blit(text2, (395, 320))

        myfont = pygame.font.SysFont("candara", 19)
        text2 = myfont.render("Cow(C) - number of matched digits in ", 1, color_tips)
        self.screen.blit(text2, (330, 350))

        myfont = pygame.font.SysFont("candara", 19)
        text2 = myfont.render("diffrent positions", 1, color_tips)
        self.screen.blit(text2, (400, 370))

        if self.wrong_input:
            myfont = pygame.font.SysFont("arialblack", 22)
            text2 = myfont.render("Wrong input!", 1, red)
            self.screen.blit(text2, (400, 260))

        surf2 = pygame.Surface((300, 180))
        surf2.fill((251, 206, 177))
        self.screen.blit(surf2, (330, 440))

        txt_surface = font.render(self.guess, True, red)
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, red, self.input_box, 2)

        self.screen.blit(self.bullImg, (-80, 90))
        self.screen.blit(self.cowImg, (480, 160))

    def write_guesses(self):
        for i in range(self.attempts, max(0, self.attempts-7), -1):
            myfont = pygame.font.SysFont("comicsansms", 20)
            s = "{} - B{}C{}".format(*self.previous_attempts[i])
            text = myfont.render(s, 1, black)
            self.screen.blit(text, (400, 450+22*(self.attempts-i)))

    def after_win(self):
        myfont = pygame.font.SysFont("gabriola", 40)
        s = "You guessed {} with {} attempts!".format(self.to_guess, self.attempts)
        if self.attempts <= 5:
            s += " Good job!"
        elif self.attempts <= 12:
            s += " Not bad!"
        else:
            s += " Try to improve!"
        text = myfont.render(s, 1, color_win)
        self.screen.blit(text, (250, 150))

        myfont2 = pygame.font.SysFont("georgia", 19)
        text2 = myfont2.render("New game - space, Exit - Esc", 1, red)
        self.screen.blit(text2, (360, 270))


if __name__ == '__main__':
    Game()