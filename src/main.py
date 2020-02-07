import pygame
import time
import random

from pygame.locals import *
from hand import HandTracking
from ingredient_button import IngredientButton
from refill_button import IngredientRefillButton
from recipe_book import RecipeBookWindow
from client import Client
from gui import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Game:    
    ingredients_file_names = [ 'b_Coca_Cola', 'b_Diet_Coke', 'b_Sprite', 'b_Pork2', 'b_Sausage1', 'b_Cheese2', 'b_Fries2', 'b_Bread', 'b_Kroket3' ]
    sounds_file_names = [ 'POL-funk-break-short.wav', 'POL-80s-pop-short.wav', 'POL-love-line-short.wav' ]
    max_number_of_clients = 6
    max_number_of_slots = 4
 
    def __init__(self, width, height): 
        self.running = True
        self.max_levels = 3
        self.number_of_minutes_per_level = 2
        self.pause = True
        self.width = width
        self.height = height
        self.wait_time = 0

        self.ingredients_buttons = []
        self.refill_buttons = []
        self.ingredients_counters = []
        self.refill_prices = []
        self.ingredients_stock = [ 5, 5, 5, 5, 5, 5, 5, 5, 5 ]
        self.ingredients_queue = []
        self.ingredients_price = [ 10, 10, 10, 15, 15, 15, 20, 20, 20 ]
        self.tray_slots = []
        self.clients_image_ids = [-1, -1, -1, -1, -1, -1]
        
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Burger Express')
        pygame.mouse.set_visible(False)
        self.hand_track = HandTracking(50)
        self.hand_cursor = HandCursor(self.hand_track)

        self.clients_orders = [ 0, 0, 0, 0, 0, 0 ]
        self.clients_type = [ 0, 0, 0, 0, 0, 0 ]
        self.clients_waiting_time = [ -1, -1, -1, -1, -1, -1 ]
        self.clients_dish_preference = []
        self.clients_remaining_time = []
        
        self.dish_price = [ 3, 3, 4, 4, 5, 4, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 5, 5, 5, 6, 6, 6]

	#				  [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 ]
        # list of dishes:
        # 
        # 1 Fries
        # 2 Kroket
        # 3 Broodje kroket
        # 4 Hamburger
        # 5 Cheeseburger
        # 6 Hotdog
        # 7 Coca Cola
        # 8 Sprite
        # 9 Diet Coke
        # 10 Kroket & Coca Cola
        # 11 Kroket & Diet Coke
        # 12 Kroket & Sprite
        # 13 Hamburger & Coca Cola
        # 14 Hamburger & Diet Coke
        # 15 Hamburger & Sprite
        # 16 Cheeseburger & Coca Cola
        # 17 Cheeseburger & Diet Coke
        # 18 Cheeseburger & Sprite
        # 19 Broodje kroket & Coca Cola
        # 20 Broodje kroket & Diet Coke
        # 21 Broodje kroket & Sprite
        # 22 Hamburger & fries & Coca Cola
        # 23 Hamburger & fries & Diet Coke
        # 24 Hamburger & fries & Sprite
        
        # ===
        
        self.level = 1
        self.money = 0
        self.max_number_of_unsatisfied_customers = 3
        self.unsatisfied_customers = 0        
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.show_ingredients_to_order = False
        self.show_recipe_book = False
        self.show_welcome_window = True
        self.win_lost_widget = WinLostWidget(self)
        
        number_of_ingredients = len(Game.ingredients_file_names)
        
        for index in range(0, number_of_ingredients / 3):
            # Buttons from the bottom-left corner            
            
            file_name = Game.ingredients_file_names[index * 3]
            position = (1, self.background.get_height() - (index + 1) * 79 - 2)
            button_left = IngredientButton(index * 3, file_name, position, self)
            counter_left = IngredientCounterWidget(index * 3, self, button_left.rect.bottomright)  
            
            file_name = Game.ingredients_file_names[index * 3 + 1]
            position = (80, self.background.get_height() - (index + 1) * 79 - 2)
            button_middle = IngredientButton(index * 3 + 1, file_name, position, self)
            counter_middle = IngredientCounterWidget(index * 3 + 1, self, button_middle.rect.bottomright)

            file_name = Game.ingredients_file_names[index * 3 + 2]
            position = (159, self.background.get_height() - (index + 1) * 79 - 2)
            button_right = IngredientButton(index * 3 + 2, file_name, position, self)
            counter_right = IngredientCounterWidget(index * 3 + 2, self, button_right.rect.bottomright)

            self.ingredients_buttons.append(button_left)
            self.ingredients_buttons.append(button_middle)
            self.ingredients_buttons.append(button_right)
            self.ingredients_counters.append(counter_left)
            self.ingredients_counters.append(counter_middle)
            self.ingredients_counters.append(counter_right)
            
            # Buttons from the middle
            
            file_name = Game.ingredients_file_names[index * 3]
            position = (self.background.get_width() / 2 - 119, self.background.get_height() / 2 + 39 - index * 79)
            button_left = IngredientRefillButton(index * 3, file_name, position, self)
            price_left = IngredientPriceWidget(index * 3, self, button_left.rect.bottomright)  
            
            file_name = Game.ingredients_file_names[index * 3 + 1]
            position = (self.background.get_width() / 2 - 40, self.background.get_height() / 2 + 39 - index * 79)
            button_middle = IngredientRefillButton(index * 3 + 1, file_name, position, self)
            price_middle = IngredientPriceWidget(index * 3 + 1, self, button_middle.rect.bottomright)

            file_name = Game.ingredients_file_names[index * 3 + 2]
            position = (self.background.get_width() / 2 + 39, self.background.get_height() / 2 + 39 - index * 79)
            button_right = IngredientRefillButton(index * 3 + 2, file_name, position, self)
            price_right = IngredientPriceWidget(index * 3 + 2, self, button_right.rect.bottomright)

            self.refill_buttons.append(button_left)
            self.refill_buttons.append(button_middle)
            self.refill_buttons.append(button_right)
            self.refill_prices.append(price_left)
            self.refill_prices.append(price_middle)
            self.refill_prices.append(price_right)

        self.restaurant_counter = RestaurantCounter(self)
        self.restaurant_kitchen = RestaurantKitchen(self)
        self.kitchen_tray = KitchenTray(self)
        self.cancel_button = CancelButton(self)
        self.phone_button_widget = PhoneButtonWidget(self)
        self.recipe_book_window = RecipeBookWindow(self)
        self.question_mark_widget = QuestionMarkWidget(self)
        self.welcome_message_window = WelcomeMessageWindow(self)

        self.money_timer_widget = MoneyTimerWidget(self)
        self.customer_satisfcation_widget = CustomerSatisfactionWidget(self)
        self.background.blit(self.money_timer_widget.image, self.money_timer_widget.rect)

        self.clients_sprites = pygame.sprite.Group()

        for table_slot in range(0, Game.max_number_of_slots):
            slot = TraySlot(table_slot, self)
            self.tray_slots.append(slot)

        for table_number in range(0, Game.max_number_of_clients):
            client = Client(table_number, self)
            dish = DishPreferenceWidget(table_number, self)
            remaining_time = DishPreferenceCounter(table_number, self)
            self.clients_sprites.add(client)
            self.clients_dish_preference.append(dish)
            self.clients_remaining_time.append(remaining_time)

        self.other_sprites = pygame.sprite.OrderedUpdates((self.restaurant_counter, self.restaurant_kitchen, self.kitchen_tray, self.cancel_button, self.phone_button_widget, self.question_mark_widget, self.tray_slots, self.money_timer_widget, self.customer_satisfcation_widget, self.clients_dish_preference, self.clients_remaining_time, self.ingredients_buttons, self.ingredients_counters, self.refill_buttons, self.refill_prices, self.recipe_book_window, self.welcome_message_window, self.win_lost_widget, self.hand_cursor))
        self.background.fill((255, 255, 255))

        self.elapsed = 0
        self.minutes = 0
        self.seconds = 0
        self.time_start = time.time()
        self.time_until_new_clients = 3
        
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound('../sounds/' + self.sounds_file_names[self.level - 1])
        self.background_music.play(-1)

    def GetInputData(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_TAB:
                    if self.pause == False:
                        if self.hand_cursor.MouseModeActivated() == True:
                            self.hand_cursor.ActivateMouseMode(False)
                        else: 
                            self.hand_cursor.ActivateMouseMode(True)
            elif event.type == MOUSEBUTTONDOWN:
                self.hand_cursor.Grab()
                self.phone_button_widget.OnMouseDown()
                self.question_mark_widget.OnMouseDown()
                self.welcome_message_window.OnMouseDown()                
                
                for ingredient_button in self.ingredients_buttons:
                    ingredient_button.OnMouseDown()
                    
                for refill_button in self.refill_buttons:
                    refill_button.OnMouseDown()

                for client in self.clients_sprites:
                    client.OnMouseDown()

                if self.cancel_button.mouse_over == True and len(self.ingredients_queue) > 0:
                    self.ingredients_queue = []
                    
                if self.show_ingredients_to_order == True and self.phone_button_widget.mouse_over == False:
                    self.show_ingredients_to_order = False
                    self.pause = False

                if self.show_recipe_book == True and self.question_mark_widget.mouse_over == False:
                    self.show_recipe_book = False
                    self.pause = False
                    
                    
            elif event.type == MOUSEBUTTONUP:
                self.hand_cursor.Release()

    def UpdateTimeVectors(self):
        for client_index in range(0, Game.max_number_of_clients):
            if self.clients_waiting_time[client_index] > 0:
                self.clients_waiting_time[client_index] -= 1
                
    def ResetWidgets(self):
        self.ingredients_stock = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self.ingredients_queue = []
        self.clients_orders = [ 0, 0, 0, 0, 0, 0 ]
        self.clients_type = [ 0, 0, 0, 0, 0, 0 ]
        self.clients_waiting_time = [ -1, -1, -1, -1, -1, -1 ]
        self.clients_dish_preference = []
        self.clients_remaining_time = []
        self.money = 0
                
    def ProcessInputData(self):
        if self.unsatisfied_customers == self.max_number_of_unsatisfied_customers:
            
            if self.pause == False:
                self.ResetWidgets()
                self.pause = True
                self.background_music.stop()
                self.background_music = pygame.mixer.Sound('../sounds/ThePriceIsRight-LoserHorns.wav')
                self.background_music.play()
        
        if self.pause == False:
            if self.time_until_new_clients == 0:
                self.time_until_new_clients = random.randint(1, 5)  # maybe we can let the time be inlfuenced by the level of the game (easy->longer time)
                                
                available_places = [i for i in range(len(self.clients_orders)) if self.clients_orders[i] == 0]
                number_of_available_places = len(available_places)
                
                if number_of_available_places > 0:  # if there are available places, generate a new client
                
                #    for each new client, generate a mood, meal order and table poisition 
                    client_mood = random.randint(1, 3)
                    random_position = random.randint(0, number_of_available_places-1)
                    table_number = available_places[random_position]
                    self.clients_type[table_number] = client_mood
                    self.clients_orders[table_number] = random.randint((self.level - 1) * 8 + 1, self.level * 8)     # this might need to change later on, so that a new client can order anything
                    self.clients_waiting_time[table_number] = (25 - client_mood*3) # 13 / 10 / 7 seconds
                    
                    print "A new client showed up at table position: " + str(table_number)
            #    now update available_places and number_of_available_places
                    available_places = [i for i in range(len(self.clients_orders)) if self.clients_orders[i] == 0]
                    number_of_available_places = len(available_places)
                    
            for table_number in range(0, Game.max_number_of_clients):
                if self.clients_waiting_time[table_number] == 0:
                    
                    # ----------------------------------------                    
                    
                    # Uncomment this and a customer that is not served in time will become unsatisfied
                    
                    if self.clients_orders[table_number] > 0:
                        self.unsatisfied_customers += 1
                        fail_sound = pygame.mixer.Sound('../sounds/Wheel-of-Fortune-Buzzer.wav')
                        fail_sound.play()
                        
                    # ---------------------------------------- 
                        
                    self.clients_type[table_number] = 0
                    self.clients_orders[table_number] = 0
                    self.clients_waiting_time[table_number] = -1
                    print 'Client {0} left the table -> {1}'.format(str(table_number), str(self.clients_orders))
        
            if int(time.time() - self.time_start) != self.elapsed:                               
                self.elapsed = int(time.time() - self.time_start)
                
                if self.seconds == 59:
                    self.seconds = 0
                    self.minutes +=1
                else:
                    self.seconds += 1

                self.time_until_new_clients -= 1
                self.wait_time -= 1
                
                if (self.minutes // self.number_of_minutes_per_level) + 1 > self.level: # New level
                    self.level = (self.minutes // self.number_of_minutes_per_level) + 1
                    self.background_music.stop()
                    self.background_music = pygame.mixer.Sound('../sounds/' + self.sounds_file_names[(self.level - 1) % self.max_levels])
                    self.background_music.play(-1)
                    
                self.UpdateTimeVectors()
                
                if self.level == self.max_levels + 1:
                    self.ResetWidgets()
                    self.pause = True
                
    def DrawOnScreen(self):
        self.clients_sprites.update()
        self.other_sprites.update()
        self.screen.blit(self.background, (0, 0))
        self.clients_sprites.draw(self.screen)
        self.other_sprites.draw(self.screen)
        pygame.display.flip() 

    def run(self):        
        
        while self.running:
            self.GetInputData()
            self.ProcessInputData()
            self.DrawOnScreen()
           
if __name__ == "__main__":
    game = Game(1200, 700)
    game.run()
