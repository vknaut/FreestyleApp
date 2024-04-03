import os
import pygame
import random  
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils.Button import Button
from utils.utils import PINK,RED,YELLOW,DARK_GREEN,DARK_GREEN2,MARINE,LIGHT_BLUE,SAND,GREY,WHITE,BLACK,ORANGE,LIGHTER_ORANGE,PEACH, colorDict, DARKER_GREY
from utils.Label import Label

class FreestyleApp:
    def __init__(self):
        self.words = self.load_words()
        self.rhymes = self.load_rhymes()
        self.current_word_index = 0
        # self.prev_word_index = 0
        self.seen_words = [] # TODO: CREATE A LOGIC AND USE THIS TO STORE THE seen_words CALLSTACK 
        self.showing_controls = False
        self.pygame_init()

        # instantiate labels and buttons
        self.current_word_label = Label("", self.big_font, BLACK, (325, 100))
        self.timer_label = Label("", self.text_font, BLACK, (50, 380))
        self.controls_info_label = Label("", self.ctrls_txt_font, BLACK, (105,100),1)
        
        #frames
        self.bottom_section_frame = pygame.Rect(0, 333, self.screen.get_width(), 300) 
        self.rhyme_section_frame = pygame.Rect(0, 470, 220, 220)      # Rhyme related button frame (left)


        # Left aligned buttons
        self.add_rhyme_button = Button(25, 480, 200, 30, "Add rhyme", MARINE, LIGHT_BLUE, self.add_rhyme, WHITE)
        self.edit_rhyme_button = Button(25, 515, 200, 30, "Edit rhyme", MARINE, LIGHT_BLUE, self.edit_rhyme, WHITE)
        self.delete_rhyme_button = Button(25, 550, 200, 30, "Delete rhyme", MARINE, LIGHT_BLUE, self.delete_rhyme, WHITE)
        self.change_timer_button = Button(25, 400, 150, 40, "Change timer",  SAND, YELLOW, self.change_interval, BLACK)

        # Center buttons
        self.get_rand_word_btn =  Button(340,400,120,40, "Random WORD", LIGHTER_ORANGE,PEACH, self.get_random_word, BLACK)
        
        # Right aligned buttons at x~666
        self.add_word_button = Button(666,480,120,30, "Add word", SAND, YELLOW, self.add_word, BLACK)
        self.edit_word_button = Button(666,515,120,30, "Edit word", SAND, YELLOW, self.edit_word, BLACK)
        self.delete_word_button = Button(666,550,120,30, "Delete word", SAND, YELLOW, self.delete_word, BLACK)

        self.show_controls_button = Button(666, 10, 120 , 30, "Show controls", SAND, YELLOW, self.show_controls)
    
    def pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Freestyle Helper")
        self.big_font = pygame.font.Font("./assets/Antonio-Bold.ttf", 46)  
        self.button_font = pygame.font.Font("./assets/Antonio-Regular.ttf", 22)
        self.text_font = pygame.font.Font(None, 24)
        self.ctrls_txt_font = pygame.font.Font("./assets/Antonio-Regular.ttf", 24)

    def show_controls(self):
        self.showing_controls = not self.showing_controls



    def cycle_to_next_word(self):
        self.current_word_index += 1
        current_word = self.words[self.current_word_index]
        print(f"Cycled to next word ({current_word}) with index:  {self.current_word_index}")
        
    def cycle_to_prev_word(self):
        self.current_word_index -= 1
        current_word = self.words[self.current_word_index]
        print(f"Cycled to previous word ({current_word}) with index: {self.current_word_index}")

    def get_random_word(self):
        # self.prev_word_index = self.current_word_index
        self.current_word_index = random.randint(0, len(self.words) - 1)

        # # TODO: Add logic to cycle through the previously seen random words callstack
        # self.seen_words.append(self.current_word_index)
        # # 

    # def prev_word(self):
    #     self.current_word_index = self.prev_word_index

    def set_timer_interval(self, interval):
        self.timer_interval = interval

    def load_words(self):
        with open('./words/CollectedWords.txt', 'r',encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def load_rhymes(self):
        rhymes = {}
        for word in self.words:
            rhyme_file_path = f'./rhymes/{word}.txt'
            if os.path.exists(rhyme_file_path):
                with open(rhyme_file_path, 'r') as file:
                    rhymes[word] = [line.strip() for line in file.readlines()]
        return rhymes

    
    def display_word_and_rhymes(self, remaining_time):
        self.screen.fill(DARKER_GREY)
        current_word = ""
        if self.words and self.showing_controls:
            self.controls_info_label.update_text("Keyboard Controls:\n             Press 'ENTER' for new Random Word\n             Press 'M' to toggle timed mode.\n             Press 'SPACE' to pause in timed mode.\n             Press 'C' to toggle Keyboard controls on/off \n       <----'LEFT_ARROWKEY' previous word | next word 'RIGHT_ARROWKEY'---->")

        elif self.words:
            current_word = self.words[self.current_word_index]
            self.current_word_label.update_text(current_word)  
            self.controls_info_label.update_text("")

        if not self.showing_controls:
            # rhyme display
            rhyme_start_x = 20  #  x 
            rhyme_y = 200  #  y 
            rhyme_spacing_x = 10  #  between rhymes spacing
            rhyme_max_width = self.screen.get_width() - 20  # Maximum width for a line
            current_x = rhyme_start_x

        if current_word in self.rhymes:
            for index, rhyme in enumerate(self.rhymes[current_word]):
                rhyme_surface = self.text_font.render(rhyme, True, (0, 10, 0))
                rhyme_width, rhyme_height = rhyme_surface.get_size()
                if current_x + rhyme_width > rhyme_max_width:
                    # if this rhyme would exceed the max width -> next line 
                    rhyme_y += rhyme_height + 10 
                    current_x = rhyme_start_x  
                
                self.screen.blit(rhyme_surface, (current_x, rhyme_y))
                current_x += rhyme_width + rhyme_spacing_x   

        # Draw Frames
        pygame.draw.rect(self.screen,DARK_GREEN, self.bottom_section_frame)
        pygame.draw.rect(self.screen,BLACK, self.rhyme_section_frame)


        # Draw Buttons
        self.add_rhyme_button.draw(self.screen)
        self.edit_rhyme_button.draw(self.screen)
        self.delete_rhyme_button.draw(self.screen)
        self.change_timer_button.draw(self.screen)
        self.get_rand_word_btn.draw(self.screen)
        self.add_word_button.draw(self.screen)
        self.edit_word_button.draw(self.screen)
        self.delete_word_button.draw(self.screen)
        self.show_controls_button.draw(self.screen)
        # Draw labels
        # Timer
        if remaining_time is not None:
            self.timer_label.update_text(f'Next word in: {remaining_time}s')
            self.timer_label.draw(self.screen)
        # Draw the appropriate label based on whether controls are being shown
        if self.showing_controls:
            self.controls_info_label.draw(self.screen)
        else:
            self.current_word_label.draw(self.screen)
   
        pygame.display.flip()

    def run(self):
        timed_mode = False
        paused = False
        timer_event = pygame.USEREVENT + 1
        self.timer_interval = 5000
        start_time = None  

        running = True
        while running:
            current_time = pygame.time.get_ticks()  
            remaining_time = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Keypress events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if timed_mode:
                            paused = not paused
                            if paused:
                                print("paused.")
                                pygame.time.set_timer(timer_event, 0)
                            else:
                                print("unpaused.")
                                start_time = pygame.time.get_ticks()  # restart timer
                                pygame.time.set_timer(timer_event, self.timer_interval) 
                        else:
                            print("Pausing only works in 'Timed' mode.\nChange Mode with Keyboard key [M].")
                               
                    elif event.key == pygame.K_m:
                        timed_mode = not timed_mode
                        if timed_mode:
                            print("Timed mode.")
                            start_time = pygame.time.get_ticks()  
                            pygame.time.set_timer(timer_event, self.timer_interval) 
                            paused = False  
                        else:
                            print("Timer deactivated.")
                            pygame.time.set_timer(timer_event, 0)

                    elif event.key == pygame.K_LEFT: 
                        self.cycle_to_prev_word()

                    elif event.key == pygame.K_RIGHT:
                        self.cycle_to_next_word()
                    
                    elif event.key == pygame.K_RETURN:
                        self.get_random_word()
                    
                    elif event.key == pygame.K_c:
                        self.show_controls()


		        # click events
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if self.add_rhyme_button.collidepoint(event.pos):
                    #     self.add_rhyme()
                    # if self.edit_rhyme_button.collidepoint(event.pos):
                    #     self.edit_rhyme()
                    # if self.delete_rhyme_button.collidepoint(event.pos):
                    #     self.delete_rhyme()
                    # if self.get_rand_word_btn.collidepoint(event.pos):
                    #     self.get_random_word()
                    # if self.change_timer_button.collidepoint(event.pos):
                    #     self.change_interval()
                    # pass
                elif event.type == timer_event:
                    self.get_random_word()
                    start_time = pygame.time.get_ticks()
                else:
                    self.add_rhyme_button.handle_event(event)
                    self.edit_rhyme_button.handle_event(event)
                    self.delete_rhyme_button.handle_event(event)
                    self.change_timer_button.handle_event(event)
                    self.get_rand_word_btn.handle_event(event)
                    self.add_word_button.handle_event(event)
                    self.edit_word_button.handle_event(event)
                    self.delete_word_button.handle_event(event)
                    self.show_controls_button.handle_event(event)
                    
            if timed_mode and not paused and start_time is not None:
                remaining_time = max(0, (((start_time + self.timer_interval) - current_time) // 1000)+1)


            self.display_word_and_rhymes(remaining_time)
            # pygame.time.wait(100)

        pygame.quit()
    
    def add_word(self):
        pass

    def delete_word(self):
        pass
    
    def edit_word(self):
        pass

    def edit_rhyme(self):
        current_word = self.words[self.current_word_index]
        if current_word in self.rhymes and self.rhymes[current_word]:
            rhyme_to_edit = simpledialog.askstring("Reim bearbeiten", f"Wählen Sie den Reim zum Bearbeiten:{self.rhymes[current_word]}")
            if rhyme_to_edit in self.rhymes[current_word]:
                new_rhyme = simpledialog.askstring("Neuer Reim", "Neuer Reim für \"" + rhyme_to_edit + "\":")
                if new_rhyme:
                    index = self.rhymes[current_word].index(rhyme_to_edit)
                    self.rhymes[current_word][index] = new_rhyme
                    self.update_rhyme_file(current_word)
            else:
                messagebox.showinfo("Information", "Keine Reime zum Bearbeiten vorhanden.")

    def add_rhyme(self):     
        current_word = self.words[self.current_word_index]
        new_rhyme = simpledialog.askstring("Neuer Reim", "Geben Sie einen Reim ein:")        
        if new_rhyme:
            if current_word in self.rhymes:
                self.rhymes[current_word].append(new_rhyme)
            else:
                self.rhymes[current_word] = [new_rhyme]
            with open(f'./rhymes/{current_word}.txt', 'a', encoding='utf-8') as file:
                file.write(f'{new_rhyme}\n')

    def delete_rhyme(self):
        current_word = self.words[self.current_word_index]
        if current_word in self.rhymes and self.rhymes[current_word]:
            rhyme_to_delete = simpledialog.askstring("Reim löschen", "Wählen Sie den Reim zum Löschen:")
            if rhyme_to_delete in self.rhymes[current_word]:
                self.rhymes[current_word].remove(rhyme_to_delete)
                self.update_rhyme_file(current_word)
            else:
                messagebox.showinfo("Information", "Keine Reime zum Löschen vorhanden.")

    def update_rhyme_file(self, word):
        with open(f'./rhymes/{word}.txt', 'w', encoding='utf-8') as file:
            for rhyme in self.rhymes[word]:
                file.write(f'{rhyme}\n')

    def change_interval(self):
        new_interval_str = simpledialog.askstring("Change Timer Interval", "Enter new interval in seconds:")
        try:
            new_interval = int(new_interval_str) * 1000  # Convert seconds to milliseconds
            if new_interval > 0:
                self.timer_interval = new_interval
                messagebox.showinfo("Timer Updated", f"Timer interval has been updated to {new_interval // 1000} seconds.")
            else:
                messagebox.showerror("Error", "Please enter a positive integer.")
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")

if __name__ == "__main__":
    app = FreestyleApp()
    app.run()