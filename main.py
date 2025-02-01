import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random
import os
from collections import defaultdict

class DataManager:
    """Handles loading, saving, and managing word and rhyme data."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.words = {}
        self.rhymes = defaultdict(list)
        self.load_data()

    def load_data(self):
        """Load data from a JSON file."""
        if not os.path.exists(self.file_path):
            # File does not exist, create it with initial data
            initial_data = {
                "words": [
                    {"id": 1, "word": "Haus"},
                    {"id": 2, "word": "Maus"}
                ],
                "rhymes": {
                    "1": [2],
                    "2": [1]
                }
            }
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(initial_data, file, ensure_ascii=False, indent=4)
            data = initial_data
        else:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to load data. The JSON file is corrupted.")
                data = {"words": [], "rhymes": {}}
        self.words = {int(item['id']): item['word'] for item in data['words']}
        self.rhymes = defaultdict(list, {k: v for k, v in data['rhymes'].items()})

    def save_data(self):
        """Save data to a JSON file."""
        data = {
            "words": [{"id": word_id, "word": word} for word_id, word in self.words.items()],
            "rhymes": {k: v for k, v in self.rhymes.items()}
        }
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_new_word_id(self):
        """Generate a new unique word ID."""
        return max(self.words.keys(), default=0) + 1

    def word_exists(self, word):
        """Check if a word already exists."""
        return word in self.words.values()

    def get_word_id(self, word):
        """Get the ID of a word."""
        for id, w in self.words.items():
            if w == word:
                return id
        return None

class SongTextManager:
    """Verwaltet Songtexte in einer eigenen JSON-Datei."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.song_texts = []
        self.load_song_texts()

    def load_song_texts(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.song_texts = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Fehler beim Laden der Songtexte. Datei beschädigt.")
                self.song_texts = []
        else:
            self.song_texts = []

    def save_song_texts(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.song_texts, file, ensure_ascii=False, indent=4)

    def add_song_text(self, title, text):
        song = {"title": title, "text": text}
        self.song_texts.append(song)
        self.save_song_texts()

    def delete_song_text(self, index):
        if 0 <= index < len(self.song_texts):
            del self.song_texts[index]
            self.save_song_texts()

    def edit_song_text(self, index, new_title, new_text):
        if 0 <= index < len(self.song_texts):
            self.song_texts[index] = {"title": new_title, "text": new_text}
            self.save_song_texts()

class RhymeDictionaryApp:
    """A GUI application for managing words and their rhymes."""

    def __init__(self, master):
        self.master = master
        master.title("Freestyle App")
        master.geometry("800x600")
        
        # Notebook erstellen und zwei Tabs hinzufügen
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        
        self.tab_dictionary = ttk.Frame(self.notebook)
        self.tab_songtext = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dictionary, text="Wörterbuch")
        self.notebook.add(self.tab_songtext, text="Songtexte")
        
        # Datenmanager initialisieren
        self.data_manager = DataManager('worte_und_reime.json')
        self.song_manager = SongTextManager('songtexte.json')
        
        # Dictionary-Tab initialisieren (hier kannst du deinen bestehenden Code adaptieren)
        self.init_dictionary_tab(self.tab_dictionary)
        
        # Songtext-Tab initialisieren
        self.init_songtext_tab(self.tab_songtext)
    def init_dictionary_tab(self, parent):
        # This label uses pack and is added directly to the tab
        label = tk.Label(parent, text="Wörterbuch Ansicht", font=("Arial", 24))
        label.pack(pady=10)
        
        # Create a dedicated frame for all grid-managed widgets
        self.dict_frame = tk.Frame(parent)
        self.dict_frame.pack(fill='both', expand=True)
        
        # Initialize state variables
        self.current_word_id = None
        self.timed_mode = False
        self.timer_interval = 5000  # in milliseconds
        self.timer_id = None
        self.showing_controls = False
        self.dictionary_view = True  # Variable to track dictionary view state

        # Create the grid-managed widgets in the dedicated frame
        self.create_widgets()
        self.bind_keys()
        self.get_random_word_id()

    
    def init_songtext_tab(self, parent):
        # Linke Seite: Listbox zur Anzeige gespeicherter Songtexte
        self.song_listbox = tk.Listbox(parent, width=30)
        self.song_listbox.pack(side='left', fill='y', padx=5, pady=5)
        self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)
        
        # Rechte Seite: Bereich zur Bearbeitung/Erstellung eines Songtexts
        edit_frame = tk.Frame(parent)
        edit_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Eingabefeld für den Titel
        tk.Label(edit_frame, text="Titel:").pack(anchor='nw')
        self.song_title_entry = tk.Entry(edit_frame)
        self.song_title_entry.pack(fill='x', pady=2)
        
        # Textfeld für den Songtext
        tk.Label(edit_frame, text="Songtext:").pack(anchor='nw')
        self.song_text_widget = tk.Text(edit_frame, wrap='word')
        self.song_text_widget.pack(fill='both', expand=True, pady=2)
        
        # Button-Frame für Aktionen
        button_frame = tk.Frame(edit_frame)
        button_frame.pack(fill='x', pady=5)
        
        tk.Button(button_frame, text="Neu", command=self.new_song).pack(side='left', padx=2)
        tk.Button(button_frame, text="Speichern", command=self.save_song).pack(side='left', padx=2)
        tk.Button(button_frame, text="Löschen", command=self.delete_song).pack(side='left', padx=2)
        tk.Button(button_frame, text="Zum Wörterbuch hinzufügen", command=self.add_words_to_dictionary).pack(side='left', padx=2)
        
        self.update_song_listbox()
    
    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for song in self.song_manager.song_texts:
            self.song_listbox.insert(tk.END, song.get("title", "Untitled"))
    
    def on_song_select(self, event):
        selection = self.song_listbox.curselection()
        if selection:
            index = selection[0]
            song = self.song_manager.song_texts[index]
            self.song_title_entry.delete(0, tk.END)
            self.song_title_entry.insert(0, song.get("title", ""))
            self.song_text_widget.delete("1.0", tk.END)
            self.song_text_widget.insert(tk.END, song.get("text", ""))
    
    def new_song(self):
        self.song_title_entry.delete(0, tk.END)
        self.song_text_widget.delete("1.0", tk.END)
        self.song_listbox.selection_clear(0, tk.END)
    
    def save_song(self):
        title = self.song_title_entry.get().strip()
        text = self.song_text_widget.get("1.0", tk.END).strip()
        if not title:
            messagebox.showerror("Error", "Bitte geben Sie einen Titel ein.")
            return
        selection = self.song_listbox.curselection()
        if selection:
            index = selection[0]
            self.song_manager.edit_song_text(index, title, text)
        else:
            self.song_manager.add_song_text(title, text)
        self.update_song_listbox()
        messagebox.showinfo("Erfolg", "Songtext gespeichert.")
    
    def delete_song(self):
        selection = self.song_listbox.curselection()
        if selection:
            index = selection[0]
            confirm = messagebox.askyesno("Bestätigung", "Möchten Sie diesen Songtext löschen?")
            if confirm:
                self.song_manager.delete_song_text(index)
                self.update_song_listbox()
                self.new_song()
                messagebox.showinfo("Erfolg", "Songtext gelöscht.")
        else:
            messagebox.showerror("Error", "Kein Songtext ausgewählt.")
    
    def add_words_to_dictionary(self):
        """
        Diese Methode soll Wörter aus dem aktuellen Songtext extrahieren und zum Wörterbuch hinzufügen.
        Hier erfolgt eine einfache Implementierung, bei der alle durch Leerzeichen getrennten Wörter geprüft werden.
        In einer erweiterten Version könnte man beispielsweise eine bessere Wortfilterung oder Interaktionsmöglichkeiten bieten.
        """
        text = self.song_text_widget.get("1.0", tk.END)
        words = text.split()
        for word in words:
            if not self.data_manager.word_exists(word):
                new_id = self.data_manager.get_new_word_id()
                self.data_manager.words[new_id] = word
        self.data_manager.save_data()
        messagebox.showinfo("Erfolg", "Wörter aus dem Songtext wurden zum Wörterbuch hinzugefügt.")
                
    def create_widgets(self):
        """Create and arrange all widgets in the dictionary frame (self.dict_frame)."""
        # Current word display
        self.current_word_label = tk.Label(self.dict_frame, text="", font=("Arial", 36))
        self.current_word_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

        # Search bar
        self.search_entry = tk.Entry(self.dict_frame)
        self.search_entry.grid(row=1, column=0, padx=10, sticky="ew")
        self.search_entry.bind('<Return>', self.search_word)

        self.search_button = tk.Button(self.dict_frame, text="Suchen", command=self.search_word)
        self.search_button.grid(row=1, column=1, padx=10, sticky="ew")

        # Words listbox
        self.words_listbox = tk.Listbox(self.dict_frame)
        self.words_listbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.words_listbox.bind('<<ListboxSelect>>', self.on_word_select)

        self.words_scrollbar = tk.Scrollbar(self.dict_frame, orient="vertical")
        self.words_scrollbar.grid(row=2, column=0, sticky="nse")
        self.words_listbox.config(yscrollcommand=self.words_scrollbar.set)
        self.words_scrollbar.config(command=self.words_listbox.yview)

        # Rhymes display
        self.rhymes_listbox = tk.Listbox(self.dict_frame)
        self.rhymes_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.rhymes_listbox.bind('<<ListboxSelect>>', self.on_rhyme_select)

        self.rhymes_scrollbar = tk.Scrollbar(self.dict_frame, orient="vertical")
        self.rhymes_scrollbar.grid(row=2, column=1, sticky="nse")
        self.rhymes_listbox.config(yscrollcommand=self.rhymes_scrollbar.set)
        self.rhymes_scrollbar.config(command=self.rhymes_listbox.yview)

        # Rhymes label (used when dictionary view is off)
        self.rhymes_label = tk.Label(self.dict_frame, text="", font=("Arial", 18), wraplength=700)
        self.rhymes_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='n')

        # Timer label
        self.timer_label = tk.Label(self.dict_frame, text="")
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Control buttons frame
        self.controls_frame = tk.Frame(self.dict_frame)
        self.controls_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

        # Configure controls frame columns to expand
        self.controls_frame.columnconfigure(0, weight=1)
        self.controls_frame.columnconfigure(1, weight=1)
        self.controls_frame.columnconfigure(2, weight=1)
        self.controls_frame.columnconfigure(3, weight=1)
        self.controls_frame.columnconfigure(4, weight=1)

        self.get_rand_word_btn = tk.Button(self.controls_frame, text="Zufälliges Wort", command=self.get_random_word_id)
        self.get_rand_word_btn.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.add_word_button = tk.Button(self.controls_frame, text="Wort hinzufügen", command=self.add_word)
        self.add_word_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.edit_word_button = tk.Button(self.controls_frame, text="Wort bearbeiten", command=self.edit_word)
        self.edit_word_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.delete_word_button = tk.Button(self.controls_frame, text="Wort löschen", command=self.delete_word)
        self.delete_word_button.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        self.toggle_view_button = tk.Button(self.controls_frame, text="Dictionary View an/aus", command=self.toggle_dictionary_view)
        self.toggle_view_button.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

        self.add_rhyme_button = tk.Button(self.controls_frame, text="Reim hinzufügen", command=self.add_rhyme)
        self.add_rhyme_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.edit_rhyme_button = tk.Button(self.controls_frame, text="Reim bearbeiten", command=self.edit_rhyme)
        self.edit_rhyme_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.delete_rhyme_button = tk.Button(self.controls_frame, text="Reim löschen", command=self.delete_rhyme)
        self.delete_rhyme_button.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

        self.change_timer_button = tk.Button(self.controls_frame, text="Intervall setzen", command=self.change_interval)
        self.change_timer_button.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        self.show_controls_button = tk.Button(self.controls_frame, text="Tastenbelegung", command=self.show_controls)
        self.show_controls_button.grid(row=1, column=4, padx=5, pady=5, sticky='ew')

        # Quit button (it's acceptable to refer to self.master.quit here)
        self.quit_button = tk.Button(self.controls_frame, text="Beenden", command=self.master.quit)
        self.quit_button.grid(row=2, column=2, padx=5, pady=5, sticky='ew')

        # Controls info label
        self.controls_info_label = tk.Label(self.dict_frame, text="", justify=tk.LEFT)
        self.controls_info_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.update_word_listbox()
        self.update_display()

    def bind_keys(self):
        """Bind keyboard events to methods."""
        self.master.bind('<Left>', lambda e: self.cycle_to_prev_word())
        self.master.bind('<Right>', lambda e: self.cycle_to_next_word())
        self.master.bind('<Return>', lambda e: self.get_random_word_id())
        self.master.bind('m', lambda e: self.toggle_timed_mode())
        self.master.bind('c', lambda e: self.show_controls())
        self.master.bind('<space>', lambda e: self.pause_timer())

    def update_display(self):
        """Update the display elements with the current state."""
        if self.showing_controls:
            controls_text = (
                "Keyboard Controls:\n"
                "Press 'ENTER' for new Random Word\n"
                "Press 'M' to toggle timed mode.\n"
                "Press 'SPACE' to pause in timed mode.\n"
                "Press 'C' to toggle Keyboard controls on/off\n"
                "← 'LEFT_ARROWKEY' previous word | next word 'RIGHT_ARROWKEY' →"
            )
            self.controls_info_label.config(text=controls_text)
            self.current_word_label.config(text="")
            self.rhymes_listbox.delete(0, tk.END)
            self.rhymes_label.config(text="")
        else:
            current_word = self.data_manager.words.get(self.current_word_id, "")
            self.current_word_label.config(text=current_word)
            self.controls_info_label.config(text="")
            if self.dictionary_view:
                # Show listboxes and search bar
                self.show_dictionary_widgets()
                self.update_rhymes_listbox()
            else:
                # Hide listboxes and search bar
                self.hide_dictionary_widgets()
                self.display_rhymes_as_labels()

    def show_dictionary_widgets(self):
        """Show the widgets related to the dictionary view."""
        self.search_entry.grid()
        self.search_button.grid()
        self.words_listbox.grid()
        self.words_scrollbar.grid()
        self.rhymes_listbox.grid()
        self.rhymes_scrollbar.grid()
        self.rhymes_label.config(text="")  # Hide rhymes label

    def hide_dictionary_widgets(self):
        """Hide the widgets related to the dictionary view."""
        self.search_entry.grid_remove()
        self.search_button.grid_remove()
        self.words_listbox.grid_remove()
        self.words_scrollbar.grid_remove()
        self.rhymes_listbox.grid_remove()
        self.rhymes_scrollbar.grid_remove()

    def display_rhymes_as_labels(self):
        """Display rhymes as labels when dictionary view is off."""
        if self.current_word_id is not None:
            rhyme_ids = self.data_manager.rhymes.get(str(self.current_word_id), [])
            rhymes = [self.data_manager.words.get(rid, "") for rid in rhyme_ids]
            rhymes_text = ", ".join(rhymes)
            self.rhymes_label.config(text=rhymes_text)
        else:
            self.rhymes_label.config(text="")

    def update_word_listbox(self):
        """Update the word listbox with all words."""
        self.words_listbox.delete(0, tk.END)
        for word in sorted(self.data_manager.words.values()):
            self.words_listbox.insert(tk.END, word)

    def update_rhymes_listbox(self):
        """Update the rhymes listbox with rhymes of the current word."""
        self.rhymes_listbox.delete(0, tk.END)
        if self.current_word_id is not None:
            rhyme_ids = self.data_manager.rhymes.get(str(self.current_word_id), [])
            for rid in rhyme_ids:
                rhyme_word = self.data_manager.words.get(rid, "")
                self.rhymes_listbox.insert(tk.END, rhyme_word)

    def get_random_word_id(self):
        """Select a random word as the current word."""
        if self.data_manager.words:
            self.current_word_id = random.choice(list(self.data_manager.words.keys()))
            self.update_display()
            self.highlight_current_word()
        else:
            self.current_word_id = None
            self.current_word_label.config(text="Keine Wörter verfügbar.")
            self.rhymes_listbox.delete(0, tk.END)
            self.rhymes_label.config(text="")

    def cycle_to_next_word(self):
        """Cycle to the next word in the list."""
        word_ids = sorted(self.data_manager.words.keys())
        if self.current_word_id in word_ids:
            current_index = word_ids.index(self.current_word_id)
            next_index = (current_index + 1) % len(word_ids)
            self.current_word_id = word_ids[next_index]
            self.update_display()
            self.highlight_current_word()

    def cycle_to_prev_word(self):
        """Cycle to the previous word in the list."""
        word_ids = sorted(self.data_manager.words.keys())
        if self.current_word_id in word_ids:
            current_index = word_ids.index(self.current_word_id)
            prev_index = (current_index - 1) % len(word_ids)
            self.current_word_id = word_ids[prev_index]
            self.update_display()
            self.highlight_current_word()

    def toggle_timed_mode(self):
        """Toggle the timed mode on or off."""
        self.timed_mode = not self.timed_mode
        if self.timed_mode:
            self.start_timer()
        else:
            self.stop_timer()
        self.update_timer_label()

    def start_timer(self):
        """Start the timer for timed mode."""
        self.stop_timer()
        self.timer_id = self.master.after(self.timer_interval, self.timer_tick)

    def stop_timer(self):
        """Stop the timer if it is running."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def timer_tick(self):
        """Timer tick event to cycle words."""
        self.get_random_word_id()
        self.start_timer()

    def pause_timer(self):
        """Pause or resume the timer."""
        if self.timed_mode:
            if self.timer_id:
                self.stop_timer()
                self.timer_label.config(text="Paused")
            else:
                self.start_timer()
                self.update_timer_label()

    def update_timer_label(self):
        """Update the timer label to reflect the current timer state."""
        if self.timed_mode:
            self.timer_label.config(text=f"Timer interval: {self.timer_interval // 1000} seconds")
        else:
            self.timer_label.config(text="Timer is off")

    def change_interval(self):
        """Change the timer interval for timed mode."""
        new_interval_str = simpledialog.askstring("Change Timer Interval", "Enter new interval in seconds:")
        if new_interval_str is not None:
            try:
                new_interval = int(new_interval_str) * 1000  # Convert to milliseconds
                if new_interval > 0:
                    self.timer_interval = new_interval
                    messagebox.showinfo("Timer Updated", f"Timer interval has been updated to {new_interval // 1000} seconds.")
                    if self.timed_mode:
                        self.start_timer()
                    self.update_timer_label()
                else:
                    messagebox.showerror("Error", "Please enter a positive integer.")
            except (TypeError, ValueError):
                messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")

    def show_controls(self):
        """Toggle the display of keyboard controls."""
        self.showing_controls = not self.showing_controls
        self.update_display()

    def toggle_dictionary_view(self):
        """Toggle the dictionary view on or off."""
        self.dictionary_view = not self.dictionary_view
        self.update_display()

    def add_word(self):
        """Prompt the user to add a new word to the dictionary."""
        word = simpledialog.askstring("Neues Wort", "Gib das Wort ein, welches du hinzufügen möchtest.")
        if word is not None and word.strip():
            word = word.strip()
            if self.data_manager.word_exists(word):
                messagebox.showinfo("Info", f"Das Wort '{word}' existiert bereits.")
                return
            new_id = self.data_manager.get_new_word_id()
            self.data_manager.words[new_id] = word
            self.data_manager.save_data()
            self.update_word_listbox()
            messagebox.showinfo("Success", f"Wort '{word}' hinzugefügt.")
        else:
            messagebox.showerror("Error", "Kein Wort eingegeben.")

    def edit_word(self):
        """Edit the currently selected word."""
        if self.current_word_id is None:
            messagebox.showerror("Error", "Kein Wort ausgewählt.")
            return
        current_word = self.data_manager.words.get(self.current_word_id, "")
        new_word = simpledialog.askstring("Editieren", f"Editiere Wort: {current_word}")
        if new_word is not None and new_word.strip():
            new_word = new_word.strip()
            if self.data_manager.word_exists(new_word):
                messagebox.showinfo("Info", f"Das Wort '{new_word}' existiert bereits.")
                return
            self.data_manager.words[self.current_word_id] = new_word
            self.data_manager.save_data()
            self.update_word_listbox()
            self.update_display()
            messagebox.showinfo("Success", f"Wort geändert zu '{new_word}'.")
        else:
            messagebox.showerror("Error", "Kein neues Wort eingegeben.")

    def delete_word(self):
        """Delete the currently selected word from the dictionary."""
        if self.current_word_id is None:
            messagebox.showerror("Error", "Kein Wort ausgewählt.")
            return
        word_id = self.current_word_id
        word = self.data_manager.words.get(word_id, "")
        confirm = messagebox.askyesno("Bestätigung", f"Möchten Sie das Wort '{word}' wirklich löschen?")
        if confirm:
            del self.data_manager.words[word_id]
            if str(word_id) in self.data_manager.rhymes:
                del self.data_manager.rhymes[str(word_id)]
            # Remove word from rhymes
            for rhymes in self.data_manager.rhymes.values():
                if word_id in rhymes:
                    rhymes.remove(word_id)
            if self.data_manager.words:
                self.current_word_id = random.choice(list(self.data_manager.words.keys()))
            else:
                self.current_word_id = None
            self.data_manager.save_data()
            self.update_word_listbox()
            self.update_display()
            messagebox.showinfo("Success", "Wort gelöscht.")

    def add_rhyme(self):
        """Add a new rhyme to the current word."""
        if self.current_word_id is None:
            messagebox.showerror("Error", "Kein Wort ausgewählt.")
            return
        new_rhyme_word = simpledialog.askstring("Neuer Reim", "Geben Sie den neuen Reim ein:")
        if new_rhyme_word is not None and new_rhyme_word.strip():
            new_rhyme_word = new_rhyme_word.strip()
            new_rhyme_id = self.data_manager.get_word_id(new_rhyme_word)
            if new_rhyme_id is None:
                # Word does not exist, add it
                new_rhyme_id = self.data_manager.get_new_word_id()
                self.data_manager.words[new_rhyme_id] = new_rhyme_word
                self.update_word_listbox()
            # Add the rhyme to the current word's list of rhymes
            current_rhymes = self.data_manager.rhymes[str(self.current_word_id)]
            if new_rhyme_id not in current_rhymes:
                current_rhymes.append(new_rhyme_id)
            # Ensure reciprocal relationship
            new_rhyme_rhymes = self.data_manager.rhymes[str(new_rhyme_id)]
            if self.current_word_id not in new_rhyme_rhymes:
                new_rhyme_rhymes.append(self.current_word_id)
            self.data_manager.save_data()
            self.update_display()
            messagebox.showinfo("Success", f"Reim '{new_rhyme_word}' hinzugefügt.")
        else:
            messagebox.showerror("Error", "Kein Reim eingegeben.")

    def edit_rhyme(self):
        """Edit the selected rhyme."""
        if self.current_word_id is None:
            messagebox.showerror("Error", "Kein Wort ausgewählt.")
            return
        selected_rhyme_id = self.get_selected_rhyme_id()
        if selected_rhyme_id is not None:
            current_rhyme_word = self.data_manager.words[selected_rhyme_id]
            new_rhyme_text = simpledialog.askstring("Reim bearbeiten", f"Neuer Text für Reim '{current_rhyme_word}':")
            if new_rhyme_text is not None and new_rhyme_text.strip():
                new_rhyme_text = new_rhyme_text.strip()
                if self.data_manager.word_exists(new_rhyme_text):
                    messagebox.showinfo("Info", f"Das Wort '{new_rhyme_text}' existiert bereits.")
                    return
                self.data_manager.words[selected_rhyme_id] = new_rhyme_text
                self.data_manager.save_data()
                self.update_word_listbox()
                self.update_display()
                messagebox.showinfo("Success", "Reim bearbeitet.")
            else:
                messagebox.showerror("Error", "Kein neuer Reim eingegeben.")
        else:
            messagebox.showerror("Error", "Kein Reim ausgewählt.")

    def delete_rhyme(self):
        """Delete the selected rhyme from the current word."""
        if self.current_word_id is None:
            messagebox.showerror("Error", "Kein Wort ausgewählt.")
            return
        selected_rhyme_id = self.get_selected_rhyme_id()
        if selected_rhyme_id is not None:
            selected_rhyme_word = self.data_manager.words[selected_rhyme_id]
            confirm = messagebox.askyesno("Bestätigung", f"Möchten Sie den Reim '{selected_rhyme_word}' wirklich löschen?")
            if confirm:
                # Remove rhyme from current word's rhymes
                self.data_manager.rhymes[str(self.current_word_id)].remove(selected_rhyme_id)
                # Remove reciprocal rhyme
                self.data_manager.rhymes[str(selected_rhyme_id)].remove(self.current_word_id)
                self.data_manager.save_data()
                self.update_display()
                messagebox.showinfo("Success", "Reim gelöscht.")
        else:
            messagebox.showerror("Error", "Kein Reim ausgewählt.")

    def get_selected_rhyme_id(self):
        """Get the ID of the selected rhyme in the rhymes listbox."""
        selected_indices = self.rhymes_listbox.curselection()
        if selected_indices:
            selected_rhyme_word = self.rhymes_listbox.get(selected_indices[0])
            return self.data_manager.get_word_id(selected_rhyme_word)
        return None

    def on_word_select(self, event):
        """Event handler for selecting a word from the word listbox."""
        selected_indices = self.words_listbox.curselection()
        if selected_indices:
            selected_word = self.words_listbox.get(selected_indices[0])
            self.current_word_id = self.data_manager.get_word_id(selected_word)
            self.update_display()

    def on_rhyme_select(self, event):
        """Event handler for selecting a rhyme from the rhymes listbox."""
        pass  # Implement visual feedback if desired

    def search_word(self, event=None):
        """Search for a word and select it if found."""
        query = self.search_entry.get().strip()
        if query:
            for idx, word in enumerate(self.words_listbox.get(0, tk.END)):
                if word.lower() == query.lower():
                    self.words_listbox.selection_clear(0, tk.END)
                    self.words_listbox.selection_set(idx)
                    self.words_listbox.activate(idx)
                    self.current_word_id = self.data_manager.get_word_id(word)
                    self.update_display()
                    return
            messagebox.showinfo("Not Found", f"Das Wort '{query}' wurde nicht gefunden.")
        else:
            messagebox.showerror("Error", "Bitte geben Sie ein Suchwort ein.")

    def highlight_current_word(self):
        """Highlight the current word in the words listbox."""
        self.words_listbox.selection_clear(0, tk.END)
        current_word = self.data_manager.words.get(self.current_word_id, "")
        for idx, word in enumerate(self.words_listbox.get(0, tk.END)):
            if word == current_word:
                self.words_listbox.selection_set(idx)
                self.words_listbox.activate(idx)
                self.words_listbox.see(idx)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = RhymeDictionaryApp(root)
    root.mainloop()
