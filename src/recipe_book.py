import pygame
from core import LoadImage

class RecipeBookWindow(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.image_null, self.rect_null = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.image_normal, self.rect_normal = LoadImage('../images', 'paper2.png', None)        
        self.mouse_over = False
        self.image, self.rect = self.image_null, self.rect_normal
        self.rect.topleft = (self.game.background.get_width()/ 2 - 220, self.game.background.get_height() / 2 - 306)

    def __del__(self):
        self.game = None
        self.image_null, self.rect_null = None, None
        self.image_normal, self.rect_normal = None, None
        self.mouse_over = False
    
    def update(self):
        if self.game.show_recipe_book == True:
            self.image = self.image_normal
            mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
            button_x, button_y = self.rect.topleft
            button_width, button_height = self.rect.width, self.rect.height
            
            if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height / 3):
                if self.mouse_over == False:
                    self.mouse_over = True
            else:
                if self.mouse_over == True:
                    self.mouse_over = False
        else:
            self.image = self.image_null
