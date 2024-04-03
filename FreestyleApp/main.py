import os
import pygame
import random  
import tkinter as tk
from tkinter import simpledialog, messagebox

class FreestyleApp:
    def __init__(self):
        self.words = self.load_words()
        self.rhymes = self.load_rhymes()
        self.current_word_index = 0
        self.prev_word_index = 0
        self.seen_words = [] # USE THIS TO STORE THE CALLSTACK 
        self.pygame_init()
        self.add_rhyme_button = pygame.Rect(50, 400, 200, 40)
        self.edit_rhyme_button = pygame.Rect(50, 450, 200, 40)
        self.delete_rhyme_button = pygame.Rect(50, 500, 200, 40)
        self.ask_for_rhyme_button = pygame.Rect(640,525,100,40)
    
    def pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Freestyle Helper")
        self.font = pygame.font.Font(None, 46)  # Standard-Schriftart und Größe
        self.button_font = pygame.font.Font(None, 24)


    def next_word(self):
        self.prev_word_index = self.current_word_index
        self.current_word_index = random.randint(0, len(self.words) - 1)

    # TODO: Add logic to save the previously watched words
    # with callstack
    def prev_word(self):
        self.current_word_index = self.prev_word_index

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

    # def display_countdown(self, remaining_time):
    #     countdown_text = self.button_font.render(f'Next word in: {remaining_time}s', True, (255, 0, 0))
    #     countdown_rect = countdown_text.get_rect(center=(400, 590))  # Position the countdown at the bottom
    #     self.screen.blit(countdown_text, countdown_rect)
    #     pygame.display.flip() 

    def display_word_and_rhymes(self, remaining_time):
        self.screen.fill((255, 255, 255)) 
        if self.words:
            # center
            current_word = self.words[self.current_word_index]
            word_surface = self.font.render(current_word, True, (0, 0, 0))
            word_rect = word_surface.get_rect(center=(400, 100))
            self.screen.blit(word_surface, word_rect)

        # rhyme display
        rhyme_start_x = 20  # Start x pos
        rhyme_y = 200  # Start y pos
        rhyme_spacing_x = 10  # Spacing between rhymes
        rhyme_max_width = self.screen.get_width() - 20  # Maximum width for a line
        current_x = rhyme_start_x

        if current_word in self.rhymes:
            for index, rhyme in enumerate(self.rhymes[current_word]):
                rhyme_surface = self.button_font.render(rhyme, True, (0, 10, 0))
                rhyme_width, rhyme_height = rhyme_surface.get_size()
                if current_x + rhyme_width > rhyme_max_width:
                    # Move to the next line if this rhyme would exceed the max width
                    rhyme_y += rhyme_height + 10 
                    current_x = rhyme_start_x  
                
                self.screen.blit(rhyme_surface, (current_x, rhyme_y))
                current_x += rhyme_width + rhyme_spacing_x   

        pygame.draw.rect(self.screen, (130, 180, 255), self.add_rhyme_button)  
        button_text = self.button_font.render('Add Rhyme', True, (255, 255, 255))
        button_rect = button_text.get_rect(center=self.add_rhyme_button.center)
        self.screen.blit(button_text, button_rect)

        pygame.draw.rect(self.screen, (130, 180, 255), self.edit_rhyme_button)  
        edit_button_text = self.button_font.render('Edit Rhyme', True, (255, 255, 255))
        edit_button_rect = edit_button_text.get_rect(center=self.edit_rhyme_button.center)
        self.screen.blit(edit_button_text, edit_button_rect)

        pygame.draw.rect(self.screen, (130, 180, 255), self.delete_rhyme_button) 
        delete_button_text = self.button_font.render('Delete Rhyme', True, (255, 255, 255))
        delete_button_rect = delete_button_text.get_rect(center=self.delete_rhyme_button.center)
        self.screen.blit(delete_button_text, delete_button_rect)

        pygame.draw.rect(self.screen, (130, 180, 255), self.ask_for_rhyme_button)  
        btn_text = self.button_font.render('New Word', True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.ask_for_rhyme_button.center)
        self.screen.blit(btn_text, btn_rect)

        if remaining_time is not None:
            countdown_text = self.font.render(f'Next word in: {remaining_time}s', True, (255, 0, 0))
            countdown_rect = countdown_text.get_rect(center=(400, 550))  # Adjust position as needed
            self.screen.blit(countdown_text, countdown_rect)

        pygame.display.flip()

    def run(self):
        timed_mode = False
        paused = False
        timer_event = pygame.USEREVENT + 1
        self.timer_interval = 5000
        start_time = None  # Store the start time here

        running = True
        while running:
            current_time = pygame.time.get_ticks()  # Get the current time
            remaining_time = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Keypress events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if timed_mode:
                            paused = not paused
                            print("unpaused.")
                        if paused:
                            print("paused.")
                            pygame.time.set_timer(timer_event, 0)
                        else:
                            print("Timed mode.")
                            start_time = pygame.time.get_ticks()  # Restart the timer
                            pygame.time.set_timer(timer_event, self.timer_interval)    
                    elif event.key == pygame.K_m:
                        timed_mode = not timed_mode
                        if timed_mode:
                            print("Timed mode.")
                            start_time = pygame.time.get_ticks()  # Start the timer
                            pygame.time.set_timer(timer_event, self.timer_interval) 
                            paused = False  
                        else:
                            print("Timer deactivated.")
                            pygame.time.set_timer(timer_event, 0)
                    elif event.key == pygame.K_LEFT: 
                        self.next_word()
                    elif event.key == pygame.K_RIGHT:
                        self.prev_word()

		        # click events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.add_rhyme_button.collidepoint(event.pos):
                        self.add_edit_delete_rhyme()
                    if self.edit_rhyme_button.collidepoint(event.pos):
                        self.edit_rhyme()
                    if self.delete_rhyme_button.collidepoint(event.pos):
                        self.delete_rhyme()
                    if self.ask_for_rhyme_button.collidepoint(event.pos):
                        self.next_word()
                elif event.type == timer_event:
                    self.next_word()
                    start_time = pygame.time.get_ticks()
            if timed_mode and not paused and start_time is not None:
                remaining_time = max(0, ((start_time + self.timer_interval) - current_time) // 1000)


            self.display_word_and_rhymes(remaining_time)
            # pygame.time.wait(100)

        pygame.quit()

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

    def add_edit_delete_rhyme(self):     
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



if __name__ == "__main__":
    app = FreestyleApp()
    app.run()