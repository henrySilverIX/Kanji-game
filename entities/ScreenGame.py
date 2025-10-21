import pandas as pd
from tkinter import *
import pygame
import numpy as np
import os
import sys

base_path = os.path.dirname(__file__)

BACKGROUND_COLOR = "#494949"
FONT_FAMILY = "Ariel"

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.mixer.init()

class ScreenGame:
    def __init__(self, window, initial_screen, csv_file):
        self.window = window
        self.initial_screen = initial_screen
        self.part_path = csv_file
        self.parte_atual = 1

        # === Estado inicial ===
        self.erros_atual = 0
        self.botao_correto = None
        self.botoes_kanji = []

        # === Cria o frame principal ===
        self.first_grade_kanji_screen = Frame(window)

        # === Fundo ===
        bg_path = resource_path("public/img/background3.png")
        self.background_image = PhotoImage(file=bg_path)
        Label(self.first_grade_kanji_screen, image=self.background_image).place(x=0, y=0, relwidth=1, relheight=1)

        # === Carrega CSV inicial ===
        self.grade_kanji_csv = pd.read_csv(self.part_path)

        num_partes = 4

        # Divide o dataframe
        partes = np.array_split(self.grade_kanji_csv, num_partes)
        
        # Teste: mostra quantas linhas em cada parte
        for i, parte in enumerate(partes):
            print(f"Parte {i+1} tem {len(parte)} kanji")

        self.parte1 = partes[0].reset_index(drop=True)
        self.parte2 = partes[1].reset_index(drop=True)
        self.grade_kanji_csv = self.parte1


        # === Define primeira questão ===
        random_line = self.grade_kanji_csv.sample().iloc[0]
        self.kanji_atual = random_line["Kanji"]
        self.indice_atual = random_line.name

        self.question_label = Label(
            self.first_grade_kanji_screen,
            text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}",
            font=(FONT_FAMILY, 16, "bold"),
            width=20, height=4, bg="#f5be6c"
        )
        self.question_label.pack(pady=40)

        # === Cria botões ===
        self.create_kanji_buttons()

        # === Botão de voltar ===
        Button(
            self.first_grade_kanji_screen,
            text="Voltar ao menu",
            width=15, bg="#e57373",
            font=(FONT_FAMILY, 14, "bold"),
            command=self.return_main_screen
        ).place(x=1700, y=50)

        # === Define botão correto inicial ===
        self.set_correct_button()

    def create_kanji_buttons(self):
        """Cria os botões e guarda referências."""
        self.botoes_kanji = []
        if len(self.grade_kanji_csv) <= 85:
            COLS, DX, DY, X0, Y0 = 10, 100, 90, 450, 250
        else:
            COLS, DX, DY, X0, Y0 = 20, 95, 95, 20, 250

        for i, kanji in enumerate(self.grade_kanji_csv["Kanji"].to_list()):
            x = X0 + (i % COLS) * DX
            y = Y0 + (i // COLS) * DY
            btn = Button(self.first_grade_kanji_screen, text=kanji, width=4, height=2,
                         bg="#f5be6c", font=(FONT_FAMILY, 18, "bold"))
            btn.config(command=lambda k=kanji, b=btn: self.check_answer(k, b))
            btn.place(x=x, y=y)
            self.botoes_kanji.append(btn)

    def set_correct_button(self):
        """Procura e define o botão correto com base no kanji atual."""
        self.botao_correto = None
        for btn in self.botoes_kanji:
            if btn.cget("text") == self.kanji_atual:
                self.botao_correto = btn
                break
        if self.botao_correto is None:
            print(f"⚠️ Nenhum botão encontrado para o kanji correto: {self.kanji_atual}")

    def return_main_screen(self):
        self.first_grade_kanji_screen.pack_forget()
        self.initial_screen.pack(fill="both", expand=True)

    def new_question(self):
        self.erros_atual = 0
        # Se acabou o CSV atual
        if self.grade_kanji_csv.empty:
            self.parte_atual += 1

            if self.parte_atual <= len(self.partes):
                self.grade_kanji_csv = self.partes[self.parte_atual - 1]
                for child in self.first_grade_kanji_screen.winfo_children():
                    if isinstance(child, Button) and child["text"] not in ["Voltar ao menu"]:
                        child.destroy()

                self.create_kanji_buttons()
                self.question_label.config(
                    text=f"Iniciando parte {self.parte_atual}...",
                    width=40, height=4, bg="#f5be6c"
                )
                self.window.after(1000, self.new_question)
                return
            else:
                # Fim de todas as partes
                self.question_label.config(
                    text="Parabéns! Você completou todos os kanji 🎉",
                    width=40, height=4, bg="#f5be6c"
                )
                for child in self.first_grade_kanji_screen.winfo_children():
                    if isinstance(child, Button):
                        child.config(state=DISABLED)
                return


        random_line = self.grade_kanji_csv.sample().iloc[0]
        self.kanji_atual = random_line["Kanji"]
        self.indice_atual = random_line.name
        self.question_label.config(
            text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}"
        )
        if not hasattr(self, "botoes_kanji") or not self.botoes_kanji:
            self.create_kanji_buttons()
        self.set_correct_button()

    def blink_button(self, botao, cor1="red", cor2="#f5be6c", n=2):
        if n > 0:
            nova_cor = cor1 if botao.cget("bg") == cor2 else cor2
            botao.config(bg=nova_cor)
            self.window.after(300, self.blink_button, botao, cor1, cor2, n - 1)
        else:
            botao.config(bg="#f5be6c")
            botao.config(state=NORMAL)

    def check_answer(self, kanji_clicado, botao):
        if kanji_clicado == self.kanji_atual:
            pygame.mixer.music.load(resource_path("public/audio/right_answer_aud.mp3"))
            pygame.mixer.music.play()
            if self.erros_atual == 0:
                botao.config(bg="#479e0d")
            elif self.erros_atual == 1:
                botao.config(bg="#faed34")
            elif self.erros_atual == 2:
                botao.config(bg="orange")
            elif self.erros_atual == 3:
                botao.config(bg="red")
            self.erros_atual = 0
            self.grade_kanji_csv.drop(index=self.indice_atual, inplace=True)
            self.window.after(1000, self.new_question)
        else:
            self.erros_atual += 1
            pygame.mixer.music.load(resource_path("public/audio/wrong_answer_aud.mp3"))
            pygame.mixer.music.play()
            self.blink_button(botao, cor1="red", cor2="#f5be6c", n=2)
            if self.erros_atual >= 3:
                if self.botao_correto:
                    self.blink_button(self.botao_correto)
                    self.botao_correto.config(bg="red")
                else:
                    print("⚠️ Botão correto não definido")