import pygame
from pygame.locals import *
from core import LoadImage

class RestaurantCounter(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = LoadImage('../images', 'table2.png', None)
        self.rect.bottomleft = (0, game.background.get_height() - 237)
        
    def __del__(self):
        self.image, self.rect = None, None

class RestaurantKitchen(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = LoadImage('../images', 'table3.png', None)
        self.rect.topleft = (0, game.background.get_height() - 240)
        
    def __del__(self):
        self.image, self.rect = None, None

class KitchenTray(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = LoadImage('../images', 'tray.png', (0, 0, 0))
        self.rect.topleft = (280, game.background.get_height() - 230)
        
    def __del__(self):
        self.image, self.rect = None, None

class IngredientCounterWidget(pygame.sprite.Sprite):
    def __init__(self, index, game, bottom_right):
        pygame.sprite.Sprite.__init__(self)
        self.index = index
        self.game = game
        
        self.font = pygame.font.Font(None, 25)        
        self.image = self.font.render(' 10 ', True, (255, 255, 255), (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomright = bottom_right 
        
    def __del__(self):
        self.index = None
        self.game = None
        self.gone = None
        self.image, self.rect = None, None

    def update(self):
        self.image = self.font.render(' {0} '.format(str(self.game.ingredients_stock[self.index])), True, (255, 255, 255), (0, 0, 0))
        
class IngredientPriceWidget(pygame.sprite.Sprite):
    def __init__(self, index, game, position):
        pygame.sprite.Sprite.__init__(self)
        self.index = index
        self.game = game
        
        self.font = pygame.font.Font(None, 25)        
        self.image_null, self.rect_null = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.image, self.rect = self.image_null, self.rect_null
        self.position = position
        
    def __del__(self):
        self.index = None
        self.game = None
        self.font = None
        self.image_null, self.rect_null = None, None
        self.image, self.rect = None, None
        self.position = None

    def update(self):
        if self.game.show_ingredients_to_order == True:
            self.image = self.font.render(' 5x{0}$ '.format(str(self.game.ingredients_price[self.index])), True, (255, 255, 255), (0, 0, 0))            
        else:
            self.image = self.image_null
            
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.position

class MoneyTimerWidget(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(' Money: 0    Time left: 00:00 ', True, (255, 255, 255), (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topright = (game.background.get_rect().topright[0] - 30, game.background.get_rect().topright[1])
        self.rect.centery = 30
        self.game = game
        
    def __del__(self):
        self.font = None
        self.image, self.rect = None, None
        self.game = None
        
    def update(self):
        if self.game.seconds == 0:
            minutes = (self.game.number_of_minutes_per_level * self.game.level) - self.game.minutes
            seconds = 0
        else:
            minutes = (self.game.number_of_minutes_per_level * self.game.level) - self.game.minutes - 1
            seconds = 60 - self.game.seconds
        
        self.image = self.font.render(' Money: {0}    Time left: {1}:{2} '.format(str(self.game.money), str(minutes).zfill(2), str(seconds).zfill(2)), True, (255, 255, 255), (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topright = (self.game.background.get_rect().topright[0] - 30, self.game.background.get_rect().topright[1])
        self.rect.centery = 30

class HandCursor(pygame.sprite.Sprite):
    def __init__(self, hand_track):
        pygame.sprite.Sprite.__init__(self)
        self.hand_normal, self.hand_normal_rect = LoadImage('../images/Cursor', 'hand1.png', (255, 255, 255))
        self.hand_grab, self.hand_grab_rect = LoadImage('../images/Cursor', 'fist1.png', -1)
        self.hand_track = hand_track
 
        self.image, self.rect = self.hand_normal, self.hand_normal_rect
        self.grabbing = False
        self.mouse_mode = True
        self.hand_state = 0
        self.hand_state_old = 0
        #self.hand_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
    def update(self):
        if self.mouse_mode == True:
            pos = pygame.mouse.get_pos()
            self.rect.midtop = pos
        else:
            pos, hand_state = self.hand_track.GetHandPosition()
            self.hand_state_old = self.hand_state
            self.hand_state = hand_state
        #    self.hand_state.pop(0)
         #   self.hand_state.append(hand_state)

            if pos is None:
                #print "An error occured while computing the cursor position based on the hand's location. No hand contour could be found."
                pass
            else:
                self.rect.midtop = pos
                
        if self.grabbing:
            self.image, self.rect = self.hand_grab, self.hand_grab_rect
        else:
            self.image, self.rect = self.hand_normal, self.hand_normal_rect
            
    def Grab(self):
        if not self.grabbing:
            self.grabbing = True
    
    def Release(self):
        self.grabbing = 0
    
    def MouseModeActivated(self):
        return self.mouse_mode
        
    def ActivateMouseMode(self, value):
        self.mouse_mode = value

class TraySlot(pygame.sprite.Sprite):
    def __init__(self, index, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.index = index
        self.image_null, self.rect_null = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.image, self.rect = self.image_null, self.rect_null
        self.rect.topleft = (418 + (index - 1) * 85, game.background.get_height() - 162)
        
    def __del__(self):
        self.game = None
        self.index = None
        self.image_null, self.rect_null = None, None
        self.image, self.rect = None, None
        
    def update(self):
        if len(self.game.ingredients_queue) >= self.index + 1:
            self.image, self.rect = LoadImage('../images/Ingredients Border', self.game.ingredients_file_names[self.game.ingredients_queue[self.index]] + '.jpg', (0, 0, 0))
            self.rect.topleft = (418 + (self.index - 1) * 85, self.game.background.get_height() - 162)
        else:
            self.image, self.rect = self.image_null, self.rect_null

class DishPreferenceWidget(pygame.sprite.Sprite):
    def __init__(self, index, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.index = index
        self.image, self.rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.rect.topleft = (85 + index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)
        
    def __del__(self):
        self.game = None
        self.index = None
        self.image, self.rect = None
        
    def update(self):
        if self.game.clients_orders[self.index] > 0:
            self.image, self.rect = LoadImage('../images/Dishes', str(self.game.clients_orders[self.index]) + '.png', (0, 0, 0))
            self.rect.topleft = (85 + self.index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)
        elif self.game.clients_orders[self.index] == -1:
            self.image, self.rect = LoadImage('../images', 'OKSign.png', (0, 0, 0))
            self.rect.topleft = (85 + self.index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)
        elif self.game.clients_orders[self.index] == -2:
            self.image, self.rect = LoadImage('../images', 'WrongSign.png', (0, 0, 0))
            self.rect.topleft = (85 + self.index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)
        else:
            self.image, self.rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
            self.rect.topleft = (85 + self.index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)   

class DishPreferenceCounter(pygame.sprite.Sprite):
    def __init__(self, index, game):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 25)
        self.image, self.rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.rect.topleft = (85 + index * 180, game.restaurant_counter.rect.topleft[1] - 290)

        self.index = index
        self.game = game
        
    def __del__(self):
        self.fot = None
        self.image, self.rect = None
        self.index = None
        self.game = None
        
    def update(self):
        if self.game.clients_waiting_time[self.index] != -1:
            self.image = self.font.render(' {0} '.format(str(self.game.clients_waiting_time[self.index])), True, (255, 255, 255), (0, 0, 0))

        else:
            self.image, self.rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
            self.rect.topleft = (85 + self.index * 180, self.game.restaurant_counter.rect.topleft[1] - 290)

class CancelButton(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = LoadImage('../images', 'cancel.png', (255, 255, 255))
        self.rect.topleft = (self.game.kitchen_tray.rect.topright[0] + 50, self.game.kitchen_tray.rect.topright[1] + 80)
        self.mouse_over = False

    def __del__(self):
        self.game = None
        self.image, self.rect = None, None
        self.mouse_over = False
    
    def update(self):
	mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
	button_x, button_y = self.rect.topleft
	button_width, button_height = self.rect.width, self.rect.height
            
	if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height):
		if self.mouse_over == False:
                    self.mouse_over = True
	else:
                if self.mouse_over == True:
                    self.mouse_over = False

class PhoneButtonWidget(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = LoadImage('../images', 'phone3.png', (0, 0, 0))
        self.rect.topright = (self.game.background.get_width() - 150, self.game.kitchen_tray.rect.topright[1] + 80)
        self.mouse_over = False

    def __del__(self):
        self.game = None
        self.image, self.rect = None, None
        self.mouse_over = False
    
    def update(self):
	mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
	button_x, button_y = self.rect.topleft
	button_width, button_height = self.rect.width, self.rect.height
            
	if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height):
		if self.mouse_over == False:
                    self.mouse_over = True
	else:
                if self.mouse_over == True:
                    self.mouse_over = False

    def OnMouseDown(self):
        if self.mouse_over == True and self.game.pause == False:
            self.game.show_ingredients_to_order = True
            self.game.pause = True
            
            print 'You clicked on the phone button'

class CustomerSatisfactionWidget(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.game = game
        self.image = self.font.render('  Level: 1   Unsatisfied: 0/{0}  '.format(self.game.max_number_of_unsatisfied_customers), True, (255, 255, 255), (0, 0, 0))
    
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, game.background.get_rect().topright[1])
        self.rect.centery = 30
        
    def __del__(self):
        self.font = None
        self.game = None
        self.image, self.rect = None, None
        
    def update(self):
        if self.game.level == self.game.max_levels + 1:
            level = self.game.max_levels
        else:
            level = self.game.level
            
        self.image = self.font.render('  Level: {0}   Unsatisfied: {1}/{2}  '.format(str(level), str(self.game.unsatisfied_customers), str(self.game.max_number_of_unsatisfied_customers)), True, (255, 255, 255), (0, 0, 0))
        
class WinLostWidget(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.rect.topleft = (self.game.width / 2 - self.rect.width / 2, self.game.height / 2 - self.rect.height / 2)
        
    def __del__(self):
        self.game = None
        self.image, self.rect = None, None
        
    def update(self):
        if self.game.unsatisfied_customers == self.game.max_number_of_unsatisfied_customers:
            self.image, self.rect = LoadImage('../images', 'LostGame.png', None)
            self.rect.topleft = (self.game.width / 2 - self.rect.width / 2, self.game.height / 2 - self.rect.height / 2)
            
        if self.game.level == self.game.max_levels + 1:
            self.image, self.rect = LoadImage('../images', 'WinGame.png', None)
            self.rect.topleft = (self.game.width / 2 - self.rect.width / 2, self.game.height / 2 - self.rect.height / 2)

class QuestionMarkWidget(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = LoadImage('../images', 'questionmark.png', (0, 0, 0))
        self.rect.topright = (self.game.background.get_width() - 30, self.game.kitchen_tray.rect.topright[1] + 80)
        self.mouse_over = False

    def __del__(self):
        self.game = None
        self.image, self.rect = None, None
        self.mouse_over = False
    
    def update(self):
	mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
	button_x, button_y = self.rect.topleft
	button_width, button_height = self.rect.width, self.rect.height
            
	if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height):
		if self.mouse_over == False:
                    self.mouse_over = True
	else:
                if self.mouse_over == True:
                    self.mouse_over = False

    def OnMouseDown(self):
        if self.mouse_over == True and self.game.pause == False:
            self.game.show_recipe_book = True
            self.game.pause = True
            print 'You clicked on Recipe Book'

class WelcomeMessageWindow(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.image_welcome, self.rect_welcome = LoadImage('../images', 'WelcomeMessage2.png', None)
        self.image_null, self.rect_null = LoadImage('../images', 'Null.jpg', (0, 0, 0))
        self.image, self.rect = self.image_null, self.rect_welcome
        self.rect.centerx = self.game.background.get_width() / 2
        self.rect.centery = self.game.background.get_height() / 2
	self.mouse_over = False
        
    def __del__(self):
        self.game = None
        self.image_welcome, self.rect_welcome = None, None
        self.image_null, self.rect_null = None, None
        self.mouse_over = False
        
    def update(self):
        if self.game.show_welcome_window == True:
            self.image = self.image_welcome

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
            self.image = self.image_null
            
    def OnMouseDown(self):
        if self.mouse_over == True and self.game.show_welcome_window == True:
            self.game.show_welcome_window = False
            self.game.pause = False
