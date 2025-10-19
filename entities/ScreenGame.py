import pandas as pd
from tkinter import *
import pygame
import os
import sys

base_path = os.path.dirname(__file__)

BACKGROUND_COLOR = "#494949"
FONT_FAMILY = "Ariel"


# Função para encontrar arquivos corretamente
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Executável
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Script normal
        return os.path.join(os.path.abspath("."), relative_path)


pygame.mixer.init()


class ScreenGame:
    def __init__(self, window, initial_screen, parte1_csv, parte2_csv):
        self.window = window
        self.initial_screen = initial_screen

        # Cria o frame principal da tela de jogo
        self.first_grade_kanji_screen = Frame(window)

        # === Fundo ===
        background_image_path = resource_path("public/img/background3.png")
        self.background_image = PhotoImage(file=background_image_path)
        background_label = Label(self.first_grade_kanji_screen, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Carrega CSV ===
        self.parte1_path = parte1_csv
        self.parte2_path = parte2_csv

        self.parte_atual = 1

        self.grade_kanji_csv = pd.read_csv(self.parte1_path)

        # === Cria label da questão ===
        self.random_line = self.grade_kanji_csv.sample().iloc[0]
        self.kanji_atual = self.random_line["Kanji"]
        self.indice_atual = self.random_line.name

        self.question_label = Label(
            self.first_grade_kanji_screen,
            text=f"{self.random_line['Português']}\n{self.random_line['On']}\n{self.random_line['Kun']}",
            font=(FONT_FAMILY, 16, "bold"),
            width=20, height=4, bg="#f5be6c"
        )
        self.question_label.pack(pady=40)

        # === Cria botões de kanji ===
        self.create_kanji_buttons()

        # === Botão para voltar ao menu ===
        back_button = Button(
            self.first_grade_kanji_screen,
            text="Voltar ao menu",
            width=15, bg="#e57373",
            font=(FONT_FAMILY, 14, "bold"),
            command=self.return_main_screen
        )
        back_button.place(x=1700, y=50)

    # === Cria os botões dos kanjis ===
    def create_kanji_buttons(self):
        """Cria os botões dos kanji e armazena todos em self.botoes_kanji."""
        self.botoes_kanji = []  # ← guarda referência de todos os botões criados

        if len(self.grade_kanji_csv) <= 85:
            COLUNAS = 10
            ESPACAMENTO_X = 100
            ESPACAMENTO_Y = 90
            OFFSET_X = 450
            OFFSET_Y = 250
        else:
            COLUNAS = 20
            ESPACAMENTO_X = 95
            ESPACAMENTO_Y = 95
            OFFSET_X = 20
            OFFSET_Y = 250

        for i, kanji in enumerate(self.grade_kanji_csv["Kanji"].to_list()):
            x = OFFSET_X + (i % COLUNAS) * ESPACAMENTO_X
            y = OFFSET_Y + (i // COLUNAS) * ESPACAMENTO_Y

            btn = Button(
                self.first_grade_kanji_screen,
                text=kanji,
                width=4, height=2,
                bg="#f5be6c",
                font=(FONT_FAMILY, 18, "bold")
            )
            btn.config(command=lambda k=kanji, b=btn: self.check_answer(k, b))
            btn.place(x=x, y=y)

            self.botoes_kanji.append(btn)  # ← adiciona o botão à lista

    # === Funções do jogo ===
    def return_main_screen(self):
        self.first_grade_kanji_screen.pack_forget()
        self.initial_screen.pack(fill="both", expand=True)

    def new_question(self):
        # Se acabou o CSV atual
        if self.grade_kanji_csv.empty:
            if self.parte_atual == 1:
                # Troca para a parte 2
                self.parte_atual = 2
                self.grade_kanji_csv = pd.read_csv(self.parte2_path)

                # Remove os botões antigos
                for child in self.first_grade_kanji_screen.winfo_children():
                    if isinstance(child, Button) and child["text"] not in ["Voltar ao menu"]:
                        child.destroy()

                # Recria os botões da parte 2
                self.create_kanji_buttons()

                # Atualiza label
                self.question_label.config(
                    text="Segunda parte iniciada!",
                    width=40, height=4, bg="#f5be6c"
                )

                # Espera 1 segundo e mostra a nova pergunta
                self.window.after(1000, self.new_question)
                return

            else:
                # Agora sim, terminou as duas partes
                pygame.mixer.music.load(resource_path("public/audio/victory_song.mp3"))
                pygame.mixer.music.play()
                self.question_label.config(
                    text="Parabéns! Você completou todos os kanji 🎉",
                    width=40, height=4, bg="#f5be6c"
                )
                for child in self.first_grade_kanji_screen.winfo_children():
                    if isinstance(child, Button):
                        child.config(state=DISABLED)
                return

        # Continua normalmente se ainda houver kanjis
        random_line = self.grade_kanji_csv.sample().iloc[0]
        self.kanji_atual = random_line["Kanji"]
        self.indice_atual = random_line.name
        self.question_label.config(
            text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}"
        )

        # ⚙️ Garante que os botões existam antes de procurar o correto
        if not hasattr(self, "botoes_kanji") or not self.botoes_kanji:
            self.create_kanji_buttons()

        # 🔎 Agora define qual é o botão correto
        self.botao_correto = None
        for btn in self.botoes_kanji:
            if btn.cget("text") == self.kanji_atual:
                self.botao_correto = btn
                break

        if self.botao_correto is None:
            print(f"⚠️ Nenhum botão encontrado para o kanji correto: {self.kanji_atual}")


    def blink_button(self, botao, cor1="red", cor2="#f5be6c", n=6):
        """Faz o botão piscar alternando entre cor1 e cor2."""
        if n > 0:
            nova_cor = cor1 if botao.cget("bg") == cor2 else cor2
            botao.config(bg=nova_cor)
            # Chama novamente após 300ms
            self.window.after(300, self.blink_button, botao, cor1, cor2, n - 1)
        else:
            # Fixa em vermelho no final
            botao.config(bg="red")
            # Reativa o botão para seguir em frente
            botao.config(state=NORMAL)

    def check_answer(self, kanji_clicado, botao):
        # Se ainda não houver contador, cria
        if not hasattr(self, "erros_atual"):
            self.erros_atual = 0

        # Se o jogador acertou
        if kanji_clicado == self.kanji_atual:
            pygame.mixer.music.load(resource_path("public/audio/right_answer_aud.mp3"))
            pygame.mixer.music.play()

            # Define cor conforme o número de erros
            if self.erros_atual == 0:
                botao.config(bg="#479e0d")   # verde
            elif self.erros_atual == 1:
                botao.config(bg="#2d3dd1")   # azul
            elif self.erros_atual == 2:
                botao.config(bg="#faed34")   # amarelo

            # Reseta contador e avança
            self.erros_atual = 0
            self.grade_kanji_csv.drop(index=self.indice_atual, inplace=True)
            self.window.after(1000, self.new_question)

        else:
            # Jogador errou
            self.erros_atual += 1
            pygame.mixer.music.load(resource_path("public/audio/wrong_answer_aud.mp3"))
            pygame.mixer.music.play()

            botao.config(bg="#d9534f")  # vermelho claro no botão errado

            if self.erros_atual >= 3:
                # 3 erros → piscar botão correto
                self.erros_atual = 0

                if hasattr(self, "botao_correto"):
                    self.blink_button(self.botao_correto)
                    self.botao_correto.config(state=NORMAL)  # reativa o botão
                else:
                    print("⚠️ Botão correto não definido")

                # O jogador precisa clicar no botão correto para continuar
        print(self.erros_atual)

