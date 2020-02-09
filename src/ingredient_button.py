import pygame
from core import LoadImage


class IngredientButton(pygame.sprite.Sprite):
    def __init__(self, index, file_name, position, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image_normal, self.rect_normal = LoadImage(
            '../images/Ingredients Border', file_name + '.jpg', None)
        self.image_over, self.rect_over = LoadImage(
            '../images/Ingredients Border', file_name + '_over.jpg', None)

        self.mouse_over = False
        self.image, self.rect = self.image_normal, self.rect_normal
        self.rect.topleft = position
        self.index = index

    def __del__(self):
        self.game = None
        self.image_normal = None
        self.rect_normal = None
        self.image_over = None
        self.rect_over = None
        self.mouse_over = False
        self.index = None

    def update(self):
        if self.game.ingredients_stock[self.index] > 0:
            self.image, self.rect = self.image_normal, self.rect_normal
            mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
            button_x, button_y = self.rect.topleft
            button_width, button_height = self.rect.width, self.rect.height

            if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height):
                if self.mouse_over == False:
                    self.mouse_over = True
            else:
                if self.mouse_over == True:
                    self.mouse_over = False
        else:
            self.image, self.rect = self.image_over, self.rect_normal

    def OnMouseDown(self):
        if self.mouse_over == True and self.game.ingredients_stock[self.index] > 0 and len(self.game.ingredients_queue) < self.game.max_number_of_slots:
            self.game.ingredients_stock[self.index] -= 1
            self.game.ingredients_queue.append(self.index)

            swoosh_sound = pygame.mixer.Sound('../sounds/Swoosh03.wav')
            swoosh_sound.play()

            print('Ingredients queue: ', self.game.ingredients_queue)
