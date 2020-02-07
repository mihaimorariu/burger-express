import pygame
import random
from core import LoadImage
from pygame.locals import *

class Client(pygame.sprite.Sprite):
    def __init__(self, table, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.table_number = table

        self.image_no_client, self.rect_no_client = LoadImage('../images/Customers/Half Size', 'no_client.png', None)
        self.image, self.rect = self.image_no_client, self.rect_no_client
        self.rect.bottomleft = (55 + self.table_number * 180, self.game.restaurant_counter.rect.topleft[1])

        self.mouse_over = False
        self.active = False

    def __del__(self):
        self.game = None
        self.table_number = None
        self.image, self.rect = None, None
        self.image_no_client, self.rect_no_client = None, None
        self.mouse_over = False
        self.active = False
            
    def update(self):
        if self.active == False:
            if self.game.clients_orders[self.table_number] > 0: # An order has been placed by this client
                mood = self.game.clients_type[self.table_number]
                image_exists = True
                
                while (image_exists):
			image_index = random.randrange(1, 7)

			if not (mood * 10 + image_index) in self.game.clients_image_ids:
				image_exists = False
						
		self.game.clients_image_ids[self.table_number] = mood * 10 + image_index
				
                if mood == 1: # Patient client
                    file_name = 'patient' + str(image_index) + '.png'
                elif mood == 2: # Neutral client
                    file_name = 'neutral' + str(image_index) + '.png'
                elif mood == 3: # Impatient client
                    file_name = 'impatient' + str(image_index) + '.png'
                    
                self.image, self.rect = LoadImage('../images/Customers/Half Size', file_name, None)
                self.rect.bottomleft = (55 + self.table_number * 180, self.game.restaurant_counter.rect.topleft[1])
                self.active = True
        else:
            if self.game.clients_orders[self.table_number] == 0: # This client left the table
                self.image, self.rect = self.image_no_client, self.rect_no_client
                                
                #self.game.clients_dish_preference[self.table_number].image, self.game.clients_dish_preference[self.table_number].rect = LoadImage('../images', 'Null.jpg', (0, 0, 0))
                #self.game.clients_dish_preference[self.table_number].rect.topleft = (85 + self.table_number * 180, self.game.restaurant_counter.rect.topleft[1] - 290)
                self.active = False

	mouse_x, mouse_y = self.game.hand_cursor.rect.centerx, self.game.hand_cursor.rect.centery
	button_x, button_y = self.rect.topleft
	button_width, button_height = self.rect.width, self.rect.height
            
	if mouse_x in range(button_x, button_x + button_width) and mouse_y in range(button_y, button_y + button_height):
		if self.mouse_over == False:
                    self.mouse_over = True
	else:
                if self.mouse_over == True:
                    self.mouse_over = False
            
    def IsCorrectMeal(self):          
        if self.game.clients_orders[self.table_number] == 1:
            # Fries
            correct_ingredients = [6]
        elif self.game.clients_orders[self.table_number] == 2:
            # Kroket
            correct_ingredients = [8]
        elif self.game.clients_orders[self.table_number] == 3:
            # Broodje kroket
            correct_ingredients = [7, 8]
        elif self.game.clients_orders[self.table_number] == 4:
            # Hamburger
            correct_ingredients = [3, 7]
        elif self.game.clients_orders[self.table_number] == 5:
            # Cheeseburger
            correct_ingredients = [3, 5, 7]
        elif self.game.clients_orders[self.table_number] == 6:
            # Hotdog
            correct_ingredients = [4, 7]
        elif self.game.clients_orders[self.table_number] == 7:
            # Coca Cola
            correct_ingredients = [0]
        elif self.game.clients_orders[self.table_number] == 8:
            # Sprite
            correct_ingredients = [2]
        elif self.game.clients_orders[self.table_number] == 9:
            # Diet Coke
            correct_ingredients = [1]
        elif self.game.clients_orders[self.table_number] == 10:
            # Kroket & Coca Cola
            correct_ingredients = [0, 8]
        elif self.game.clients_orders[self.table_number] == 11:
            # Kroket & Diet Coke
            correct_ingredients = [1, 8]
        elif self.game.clients_orders[self.table_number] == 12:
            # Kroket & Sprite
            correct_ingredients = [2, 8]
        elif self.game.clients_orders[self.table_number] == 13:
            # Hamburger & Coca Cola
            correct_ingredients = [0, 3, 7]
        elif self.game.clients_orders[self.table_number] == 14:
            # Hamburger & Diet Coke
            correct_ingredients = [1, 3, 7]
        elif self.game.clients_orders[self.table_number] == 15:
            # Hamburger & Sprite
            correct_ingredients = [2, 3, 7]
        elif self.game.clients_orders[self.table_number] == 16:
            # Cheeseburger & Coca Cola
            correct_ingredients = [0, 3, 5, 7]
        elif self.game.clients_orders[self.table_number] == 17:
            # Cheeseburger & Diet Coke
            correct_ingredients = [1, 3, 5, 7]
        elif self.game.clients_orders[self.table_number] == 18:
            # Cheeseburger & Sprite
            correct_ingredients = [2, 3, 5, 7]
        elif self.game.clients_orders[self.table_number] == 19:
            # Broodje kroket & Coca Cola
            correct_ingredients = [0, 7, 8]
        elif self.game.clients_orders[self.table_number] == 20:
            # Broodje kroket & Diet Coke
            correct_ingredients = [1, 7, 8]
        elif self.game.clients_orders[self.table_number] == 21:
            # Broodje kroket & Sprite
            correct_ingredients = [2, 7, 8]
        elif self.game.clients_orders[self.table_number] == 22:
            # Hamburger & fries & Coca Cola
            correct_ingredients = [0, 3, 6, 7]
        elif self.game.clients_orders[self.table_number] == 23:
            # Hamburger & fries & Diet Coke
            correct_ingredients = [1, 3, 6, 7]
        else:
            # Hamburger & fries & Sprite
            correct_ingredients = [2, 3, 6, 7]
        
        self.game.ingredients_queue.sort()
        
        return self.game.ingredients_queue == correct_ingredients
        
    def OnMouseDown(self):
        if self.active == True and self.mouse_over == True:
            print 'You clicked on customer {0}.'.format(self.table_number)
            
            if len(self.game.ingredients_queue) > 0:
                
                if (self.IsCorrectMeal()):
                    print 'Correct meal'
                    self.game.clients_orders[self.table_number] = -1
                    self.game.clients_waiting_time[self.table_number] = 2
                    self.game.money += self.game.dish_price[self.game.clients_orders[self.table_number]]
                    success_sound = pygame.mixer.Sound('../sounds/cash-register2.wav')
                    success_sound.play()
                else:
                    print 'Not correct meal'
                    self.game.clients_orders[self.table_number] = -2
                    self.game.clients_waiting_time[self.table_number] = 2
                    self.game.unsatisfied_customers += 1
                    fail_sound = pygame.mixer.Sound('../sounds/Wheel-of-Fortune-Buzzer.wav')
                    fail_sound.play()

                self.game.ingredients_queue = []
