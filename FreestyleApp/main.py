import os
import pygame
import random  
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils.Button import Button
from utils.utils import colorDict
from utils.Label import Label

class FreestyleApp:
    def __init__(self):
        self.load_data_from_json('FreestyleApp/json/worte_und_reime.json')
        self.current_word_id = 1
        # self.prev_word_index = 0
        # self.seen_words = [] # TODO: CREATE A LOGIC AND USE THIS TO STORE THE seen_words CALLSTACK     
        self.showing_controls = False
        self.pygame_init()

        # instantiate labels and buttons
        self.current_word_label = Label("", self.big_font, colorDict['BLACK'], (305, 50))
        self.timer_label = Label("", self.text_font, colorDict['BLACK'], (50, 380))
        self.controls_info_label = Label("", self.ctrls_txt_font, colorDict['BLACK'], (105,100),1)
        
        #frames
        self.bottom_section_frame = pygame.Rect(0, 333, self.screen.get_width(), 300) 
        self.rhyme_section_frame = pygame.Rect(0, 470, 220, 220)      # Rhyme related button frame (left)


        # Left aligned buttons
        self.add_rhyme_button = Button(25, 480, 200, 30, "Add rhyme", colorDict['MARINE'], colorDict['LIGHT_BLUE'], self.add_rhyme, colorDict['WHITE'],"FreestyleApp/assets/img/nightblue-btn.png","FreestyleApp/assets/img/blue-btn.png","FreestyleApp/assets/img/lightblue-btn.png")
        self.edit_rhyme_button = Button(25, 515, 200, 30, "Edit rhyme", colorDict['MARINE'], colorDict['LIGHT_BLUE'], self.edit_rhyme, colorDict['WHITE'],"FreestyleApp/assets/img/nightblue-btn.png","FreestyleApp/assets/img/blue-btn.png","FreestyleApp/assets/img/lightblue-btn.png")
        self.delete_rhyme_button = Button(25, 550, 200, 30, "Delete rhyme", colorDict['MARINE'], colorDict['LIGHT_BLUE'], self.delete_rhyme, colorDict['WHITE'],"FreestyleApp/assets/img/nightblue-btn.png","FreestyleApp/assets/img/blue-btn.png","FreestyleApp/assets/img/lightblue-btn.png")
        self.change_timer_button = Button(25, 400, 150, 40, "Change timer",  colorDict['SAND'], colorDict['YELLOW'], self.change_interval, colorDict['PEACH'],"FreestyleApp/assets/img/violet-btn.png","FreestyleApp/assets/img/lightviolet-btn.png","FreestyleApp/assets/img/darkorange-btn.png")

        # Center buttons
        self.get_rand_word_btn =  Button(340,400,120,40, "Random WORD", 
                                        colorDict['SAND'],colorDict['PEACH'], 
                                        self.get_random_word_id, colorDict['WHITE'],#font-color
                                        "FreestyleApp/assets/img/violet-btn.png",
                                        "FreestyleApp/assets/img/lightviolet-btn.png",
                                        "FreestyleApp/assets/img/darkorange-btn.png")
        
        # Right aligned buttons at x~666
        self.add_word_button = Button(666,480,120,30, "Add word", 
                                      colorDict['MARINE'], colorDict['LIGHT_BLUE'], 
                                      self.add_word, colorDict['WHITE'],
                                      "FreestyleApp/assets/img/nightblue-btn.png",
                                      "FreestyleApp/assets/img/blue-btn.png",
                                      "FreestyleApp/assets/img/lightblue-btn.png")
        
        self.edit_word_button = Button(666,515,120,30, "Edit word", 
                                       colorDict['MARINE'], colorDict['LIGHT_BLUE'], 
                                       self.edit_word, colorDict['WHITE'],
                                       "FreestyleApp/assets/img/nightblue-btn.png",
                                       "FreestyleApp/assets/img/blue-btn.png",
                                       "FreestyleApp/assets/img/lightblue-btn.png")
        
        self.delete_word_button = Button(666,550,120,30, "Delete word",
                                         colorDict['MARINE'], colorDict['LIGHT_BLUE'], 
                                         self.delete_word, colorDict['WHITE'],
                                         "FreestyleApp/assets/img/nightblue-btn.png",
                                         "FreestyleApp/assets/img/blue-btn.png",
                                         "FreestyleApp/assets/img/lightblue-btn.png")

        # Top right corner
        self.show_controls_button = Button(666, 10, 120 , 30, "Show controls", 
                                           colorDict['SAND'], colorDict['YELLOW'], 
                                           self.show_controls, colorDict['PEACH'], 
                                           "FreestyleApp/assets/img/violet-btn.png",
                                           "FreestyleApp/assets/img/lightviolet-btn.png",
                                           "FreestyleApp/assets/img/darkorange-btn.png")
    
    def pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Freestyle Helper")
        self.big_font = pygame.font.Font("FreestyleApp/assets/fonts/Antonio-Bold.ttf", 46)  
        self.button_font = pygame.font.Font("FreestyleApp/assets/fonts/Antonio-Regular.ttf", 22)
        self.text_font = pygame.font.Font("FreestyleApp/assets/fonts/Antonio-Regular.ttf", 24)
        self.ctrls_txt_font = pygame.font.Font("FreestyleApp/assets/fonts/Antonio-Regular.ttf", 24)

    ####### CLASS METHODS #####
    def show_controls(self):
        self.showing_controls = not self.showing_controls

    def set_timer_interval(self, interval):
        self.timer_interval = interval

    def change_interval(self):
            new_interval_str = simpledialog.askstring("Change Timer Interval", "Enter new interval in seconds:")
            try:
                new_interval = int(new_interval_str) * 1000  # -> ms
                if new_interval > 0:
                    self.timer_interval = new_interval
                    messagebox.showinfo("Timer Updated", f"Timer interval has been updated to {new_interval // 1000} seconds.")
                else:
                    messagebox.showerror("Error", "Please enter a positive integer.")
            except (TypeError, ValueError):
                messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")


    ## JSON METHODS ############################################################
    def load_data_from_json(self, file_path='FreestyleApp/json/worte_und_reime.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.words = {item['id']: item['word'] for item in data['words']}
            self.rhymes = data['rhymes']
        
    def save_data_to_json(self, file_path='FreestyleApp/json/worte_und_reime.json'):
        data = {
            "words": [{"id": word_id, "word": word} for word_id, word in self.words.items()],
            "rhymes": self.rhymes
        }
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_random_word_id(self):
        # print(random.choice(list(self.words.keys()))) # debug
        self.current_word_id= random.choice(list(self.words.keys()))
    
    def add_word(self):
        word = simpledialog.askstring("Neues Wort", "Gib das Wort ein, welches du hinzufügen möchtest.")
        new_id = max(self.words.keys()) + 1  
        self.words[new_id] = word  
        self.rhymes[str(new_id)] = []  
        self.save_data_to_json()  


    def delete_word(self):
        word_id = self.current_word_id
        if word_id in self.words:
            self.current_word_id = 1            
            del self.words[word_id]  
            if str(word_id) in self.rhymes:
                del self.rhymes[str(word_id)]  
            self.save_data_to_json()  

    
    def edit_word(self):
        word_id = self.current_word_id
        new_word = simpledialog.askstring("Editieren",f"Editiere Wort:{self.words[word_id]}")

        if word_id in self.words and new_word:
            self.words[word_id] = new_word  
            self.save_data_to_json() 

    
    def edit_rhyme(self):
        current_word_id = self.current_word_id 
        if current_word_id is not None and str(current_word_id) in self.rhymes:
            rhyme_ids = self.rhymes[str(current_word_id)]
            if rhyme_ids:
                
                rhymes_options = ", ".join([f"{rid}: {self.words[rid]}" for rid in rhyme_ids])
                selected_rhyme_id_str = simpledialog.askstring("Reim bearbeiten", f"Wählen Sie die ID des Reims zum Bearbeiten aus den folgenden Optionen: {rhymes_options}")
                try:
                    selected_rhyme_id = int(selected_rhyme_id_str)
                    if selected_rhyme_id in rhyme_ids:
                        new_rhyme_text = simpledialog.askstring("Neuer Reim", "Geben Sie den neuen Reimtext ein:")
                        if new_rhyme_text and new_rhyme_text not in self.words.values():
                            new_rhyme_id = max(self.words.keys()) + 1
                            self.words[new_rhyme_id] = new_rhyme_text
                            
                            # Aktualisieren der Reim-IDs für das aktuelle Wort
                            self.rhymes[str(current_word_id)] = [new_rhyme_id if rid == selected_rhyme_id else rid for rid in rhyme_ids]
                            self.save_data_to_json()  # Änderungen speichern
                        else: 
                            messagebox.showinfo("Info", "Der Reimtext existiert bereits in der WortDatenbank.\nID's werden verknüpft...")
                            #TODO: IMPLEMENT: Aktualisieren der Reim-IDs -> Verküpfung der sich reimenden Wörter.
                    else:
                        messagebox.showerror("Fehler", "Ungültige Reim-ID.")
                except ValueError:
                    messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Reim-ID ein.")
            else:
                messagebox.showinfo("Information", "Keine Reime zum Bearbeiten vorhanden.")
        else:
            messagebox.showerror("Fehler", "Kein Wort ausgewählt oder keine Reime verfügbar.")


    def add_rhyme(self):
        current_word_id = self.current_word_id  # Verwendung der aktuell ausgewählten Wort-ID
        if current_word_id is not None:
            new_rhyme_text = simpledialog.askstring("Neuer Reim", "Geben Sie den neuen Reim ein:")
            if new_rhyme_text:
                # Überprüfen, ob der neue Reimtext bereits existiert. Wenn nicht, füge ihn als neues Wort hinzu.
                new_rhyme_id = None
                for id, word in self.words.items():
                    if word == new_rhyme_text:
                        new_rhyme_id = id
                        break
                if new_rhyme_id is None:  #  Reim existiert nicht -> hinzufügen
                    new_rhyme_id = max(self.words.keys()) + 1
                    self.words[new_rhyme_id] = new_rhyme_text
                
                # Reim zur Liste der Reime für das aktuelle Wort hinzufügen

                if str(current_word_id) in self.rhymes:
                    if new_rhyme_id not in self.rhymes[str(current_word_id)]:
                        for rid in self.rhymes[str(current_word_id)]:
                            self.rhymes[str(rid)].append(new_rhyme_id)
                        #TODO: LOGIK ZUM KREUZCHECKEN DER ANDEREN ID'S + HINZUFÜGEN WENN FEHLEND DAMIT AM ENDE ALLE ID'S IN JEDE RICHTUNG HIN VERKNÜPFT SIND

                        self.rhymes[str(current_word_id)].append(new_rhyme_id)

                else:
                    self.rhymes[str(current_word_id)] = [new_rhyme_id]
                
                self.save_data_to_json()  
                # messagebox.showinfo("Erfolg", "Reim erfolgreich hinzugefügt.")
                print("Reim erfolgreich hinzugefügt.")
            else:
                messagebox.showerror("Fehler", "Kein Reim eingegeben.")
        else:
            messagebox.showerror("Fehler", "Kein Wort ausgewählt.")


    def delete_rhyme(self):
        current_word_id = self.current_word_id 
        if current_word_id is not None and str(current_word_id) in self.rhymes:
            rhyme_ids = self.rhymes[str(current_word_id)]
            if rhyme_ids:
                # Erzeugen einer Auswahl an verfügbaren Reimen zum Löschen
                rhymes_options = ", ".join([f"{rid}: {self.words[rid]}" for rid in rhyme_ids])
                selected_rhyme_id_str = simpledialog.askstring("Reim löschen", f"Wählen Sie die ID des Reims zum Löschen aus den folgenden Optionen: {rhymes_options}")
                try:
                    selected_rhyme_id = int(selected_rhyme_id_str)
                    if selected_rhyme_id in rhyme_ids:
                        # Löschen des ausgewählten Reims aus der Liste der Reime für das aktuelle Wort
                        self.rhymes[str(current_word_id)].remove(selected_rhyme_id)
                        # Optional: Löschen des Wortes selbst, wenn es nur als Reim existiert und sonst nirgends referenziert wird
                        # if all(selected_rhyme_id not in rhymes for rhymes in self.rhymes.values()):
                        #     del self.words[selected_rhyme_id]

                        self.save_data_to_json()  # Änderungen speichern
                        messagebox.showinfo("Erfolg", "Reim erfolgreich gelöscht.")
                    else:
                        messagebox.showerror("Fehler", "Ungültige Reim-ID.")
                except ValueError:
                    messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Reim-ID ein.")
            else:
                messagebox.showinfo("Information", "Keine Reime zum Löschen vorhanden.")
        else:
            messagebox.showerror("Fehler", "Kein Wort ausgewählt oder keine Reime verfügbar.")



    ###### TODO: Add functionality to handle the word id's in case one word is deleted.
    def cycle_to_next_word(self):
        try:
            self.current_word_id += 1
            current_word = self.words[self.current_word_id]
            print(f"Cycled to next word ({current_word}) with index:  {self.current_word_id}")

        except:
            self.get_random_word_id()
            current_word = self.words[self.current_word_id]
            print(f"Randomly jumped to word '{current_word}' with index:  {self.current_word_id}")

    def cycle_to_prev_word(self):
        try:
            self.current_word_id -= 1
            current_word = self.words[self.current_word_id]
            print(f"Cycled to previous word ({current_word}) with index: {self.current_word_id}")
        except:
            self.get_random_word_id()
            current_word = self.words[self.current_word_id]
            print(f"Randomly jumped to word '{current_word}' with index:  {self.current_word_id}")

    ## DRAW METHOD #################################################################
    def display_word_and_rhymes(self, remaining_time):
        self.screen.fill(colorDict['DARKER_GREY'])
        # current_word_text = ""
        if self.words and self.showing_controls:
            self.controls_info_label.update_text("Keyboard Controls:\n             Press 'ENTER' for new Random Word\n             Press 'M' to toggle timed mode.\n             Press 'SPACE' to pause in timed mode.\n             Press 'C' to toggle Keyboard controls on/off \n       ←'LEFT_ARROWKEY' previous word | next word 'RIGHT_ARROWKEY'→")
        elif self.words and self.current_word_id is not None:
            # Hier nutzen wir die ID, um den Worttext zu holen.
            current_word_text = self.words[self.current_word_id]
            self.current_word_label.update_text(current_word_text)
            self.controls_info_label.update_text("")

        if not self.showing_controls and self.current_word_id is not None:
            current_word_text = self.words[self.current_word_id]
            self.current_word_label.update_text(current_word_text)
            # Reime darstellen, basierend auf den IDs
            rhyme_ids = self.rhymes.get(str(self.current_word_id), [])
            rhyme_texts = [self.words[rhyme_id] for rhyme_id in rhyme_ids]

            rhyme_start_x = 20  #x-coord
            rhyme_y = 200  # y-coord
            rhyme_spacing_x = 10 
            rhyme_max_width = self.screen.get_width() - 20  

            current_x = rhyme_start_x
            for rhyme_text in rhyme_texts:
                rhyme_surface = self.text_font.render(rhyme_text, True, (0, 10, 0))
                rhyme_width, rhyme_height = rhyme_surface.get_size()
                if current_x + rhyme_width > rhyme_max_width:
                    # Zeilenumbruch, wenn der Reim über die maximale Breite hinausgehen würde
                    rhyme_y += rhyme_height + 10
                    current_x = rhyme_start_x
                
                self.screen.blit(rhyme_surface, (current_x, rhyme_y))
                current_x += rhyme_width + rhyme_spacing_x

        # Rahmen und Steuerelemente wie zuvor zeichnen
        pygame.draw.rect(self.screen, colorDict['DARK_GREEN'], self.bottom_section_frame)
        pygame.draw.rect(self.screen, colorDict['BLACK'], self.rhyme_section_frame)

        self.add_rhyme_button.draw(self.screen)
        self.edit_rhyme_button.draw(self.screen)
        self.delete_rhyme_button.draw(self.screen)
        self.change_timer_button.draw(self.screen)
        self.get_rand_word_btn.draw(self.screen)
        self.add_word_button.draw(self.screen)
        self.edit_word_button.draw(self.screen)
        self.delete_word_button.draw(self.screen)
        self.show_controls_button.draw(self.screen)

        if remaining_time is not None:
            self.timer_label.update_text(f'Next word in: {remaining_time}s')
            self.timer_label.draw(self.screen)

        if self.showing_controls:
            self.controls_info_label.draw(self.screen)
        else:
            self.current_word_label.draw(self.screen)

        pygame.display.flip()



    # MAIN LOOP #########################################################################
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
                        self.get_random_word_id()
                    
                    elif event.key == pygame.K_c:
                        self.show_controls()

                elif event.type == timer_event:
                    self.get_random_word_id()
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
    
if __name__ == "__main__":
    app = FreestyleApp()
    app.run()