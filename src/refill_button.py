import pygame
from core import LoadImage

class IngredientRefillButton(pygame.sprite.Sprite):
    def __init__(self, index, file_name, position, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.index = index
        
        self.image_null, self.rect_null = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.image_normal, self.rect_normal = LoadImage('../images/Ingredients Border', file_name + '.jpg', None)
        self.image_over, self.rect_over = LoadImage('../images/Ingredients Border', file_name + '_over.jpg', None)
        
        self.mouse_over = False
        self.image, self.rect = self.image_null, self.rect_normal
        self.position = position
        self.phone_sound = pygame.mixer.Sound('../sounds/Ringing_Phone.wav')

        self.rect.topleft = self.position

    def __del__(self):
        self.game = None
        self.image_null, self.rect_null = None, None
        self.image_normal, self.rect_normal = None, None
        self.image_over, self.rect_over = None, None
        self.mouse_over = False
        self.phone_sound = None
        self.index = None
    
    def update(self):
        if self.game.show_ingredients_to_order == True:
            if self.game.money >= self.game.ingredients_price[self.index]:
                self.image = self.image_normal
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
                self.image = self.image_over
        else:
            self.image = self.image_null
            
    def OnMouseDown(self):
        if self.game.show_ingredients_to_order == True:
            if self.mouse_over == True and self.game.money >= self.game.ingredients_price[self.index]:
                self.game.ingredients_stock[self.index] += 5
                self.game.money -= self.game.ingredients_price[self.index]
                self.phone_sound.stop()
                self.phone_sound.play()
                self.mouse_over = False
                print 'You clicked on {0}'.format(str(self.index))
