import tkinter as tk
from tkinter import messagebox
from game import Game
from game_processing import AI

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Skaitļu virkne - Spēle")

        # Konfigurācijas loga izveide
        self.config_frame = tk.Frame(master)
        self.config_frame.pack(padx=10, pady=10)

        # Skaitļu virknes garuma ievade
        tk.Label(self.config_frame, text="Ievadiet skaitļu virknes garumu (15-25):").grid(row=0, column=0, sticky="w")
        self.length_entry = tk.Entry(self.config_frame, width=5)
        self.length_entry.grid(row=0, column=1, sticky="w")
        self.length_entry.insert(0, "20")

        # Dziļuma ierobežojums
        tk.Label(self.config_frame, text="Ievadiet pārmeklēšanās dziļuma ierobežojumu:").grid(row=0, column=2, sticky="w")
        self.depth_entry = tk.Entry(self.config_frame, width=5)
        self.depth_entry.grid(row=0, column=3, sticky="w")
        self.depth_entry.insert(0, "5")

        # Algoritma izvēle
        tk.Label(self.config_frame, text="Izvēlieties datoralgoritmu:").grid(row=1, column=0, sticky="w")
        self.algo_var = tk.StringVar(value="1")
        tk.Radiobutton(self.config_frame, text="Minimax", variable=self.algo_var, value="1").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self.config_frame, text="Alpha-Beta", variable=self.algo_var, value="2").grid(row=1, column=2, sticky="w")

        # Sākuma gājiena izvēle
        tk.Label(self.config_frame, text="Kas sāk spēli:").grid(row=2, column=0, sticky="w")
        self.start_var = tk.StringVar(value="human")
        tk.Radiobutton(self.config_frame, text="Cilvēks", variable=self.start_var, value="human").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(self.config_frame, text="Dators", variable=self.start_var, value="computer").grid(row=2, column=2, sticky="w")

        # Spēles sākšanas poga
        self.start_button = tk.Button(self.config_frame, text="Sākt spēli", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Spēles loga izveide
        self.game_frame = tk.Frame(master)
        self.score_label = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.score_label.pack(pady=5)
        self.turn_label = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.turn_label.pack(pady=5)
        self.sequence_frame = tk.Frame(self.game_frame)
        self.sequence_frame.pack(pady=10)

        self.game = None
        self.ai = None

    def start_game(self):
        try:  # Ievades validācija
            length = int(self.length_entry.get())
            depth = int(self.depth_entry.get())
            if not (15 <= length <= 25):
                messagebox.showerror("Kļūda", "Garumam jābūt no 15 līdz 25.")
                return
        except ValueError:
            messagebox.showerror("Kļūda", "Ievadiet skaitli!")
            return

        # Sākuma gājiena noteikšana
        human_starts = (self.start_var.get() == "human")

        # Spēles un AI inicializācija
        algo_choice = self.algo_var.get()
        self.game = Game(length, human_starts=human_starts)
        self.ai = AI(algo_choice)

        self.config_frame.pack_forget()
        self.game_frame.pack(padx=10, pady=10)
        self.update_game_display()

        if self.game.is_comp_turn:
            self.master.after(500, self.computer_move)

    # Spēles ekrāna atjaunināšana pēc gājieniem
    def update_game_display(self):
        score_text = f"Punkti — Cilvēks: {self.game.human_score}, Dators: {self.game.comp_score}"
        self.score_label.config(text=score_text)

        turn_text = "Tavs gājiens" if not self.game.is_comp_turn else "Datora gājiens"
        self.turn_label.config(text=turn_text)

        for widget in self.sequence_frame.winfo_children():
            widget.destroy()

        for idx, number in enumerate(self.game.sequence):
            btn = tk.Button(self.sequence_frame, text=str(number), width=3,
                            command=lambda i=idx: self.human_move(i))
            btn.grid(row=0, column=idx, padx=2, pady=2)

    # Cilvēka gājiena izpilde
    def human_move(self, index):
        if self.game.is_comp_turn:
            return

        self.game.make_move(index, is_human=True)
        self.update_game_display()

        if self.game.is_game_over():
            self.end_game()
            return

        # Datora gājiena izsaukšana
        self.master.after(500, self.computer_move)

    # Datora gājiena izpilde
    def computer_move(self):
        if not self.game.is_comp_turn or self.game.is_game_over():
            return

        index = self.ai.choose_move(self.game)
        self.game.make_move(index, is_human=False)
        self.update_game_display()

        if self.game.is_game_over():
            self.end_game()
            return

    # Spēles rezultāta izvade
    def end_game(self):
        result = f"Rezultāts — Cilvēks: {self.game.human_score}, Dators: {self.game.comp_score}\n{self.game.get_winner()}"
        messagebox.showinfo("Spēle beigusies", result)

# Funkcija GUI palaišanai

def run():
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
