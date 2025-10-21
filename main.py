from entities.ScreenGame import ScreenGame
import pygame
import pandas as pd
from tkinter import *
import os
import sys

BACKGROUND_COLOR = "#494949"
FONT_FAMILY = "Ariel"
base_path = os.path.dirname(__file__)

pygame.mixer.init()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def selecionar_kanji_csv(conjunto):
    global qual_conjunto
    qual_conjunto = conjunto  # "primeiro_ano" ou "segundo_ano"
    print(f"Conjunto selecionado: {qual_conjunto}")
    go_to_difficult_level()

# === Main Window ===
window = Tk()
window.title("Quiz Kanji")
window.minsize(width=1920, height=1080) #Estava 1920 x 1080

# === Tela inicial ===
initial_screen = Frame(window)
initial_screen.pack(fill="both", expand=True)

def go_to_difficult_level():
    initial_screen.pack_forget()
    difficult_selection_screen.pack(fill="both", expand=True)

background_image = PhotoImage(file=resource_path("public/img/background.png"))
background_label = Label(initial_screen, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Label(initial_screen, text="Quiz de Japonês - Kanji!", font=(FONT_FAMILY, 24, "bold"), bg=BACKGROUND_COLOR, fg="white").pack(pady=40)

Button(initial_screen, text="1º ano", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=lambda: selecionar_kanji_csv("primeiro_ano")).pack(pady=10)
Button(initial_screen, text="2º ano", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=lambda: selecionar_kanji_csv("segundo_ano")).pack(pady=10)
Button(initial_screen, text="3º ano", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=lambda: selecionar_kanji_csv("terceiro_ano")).pack(pady=10)
Button(initial_screen, text="Sair", width=15, bg="#e57373", font=(FONT_FAMILY, 14, "bold"), command=window.destroy).place(x=1700, y=950)







# === Tela de seleção de dificuldade ===
difficult_selection_screen = Frame(window)

def return_main_screen():
    difficult_selection_screen.pack_forget()
    initial_screen.pack(fill="both", expand=True)

background_image_difficult_screen = PhotoImage(file=resource_path("public/img/background2.png"))
background_label_difficult_screen = Label(difficult_selection_screen, image=background_image_difficult_screen)
background_label_difficult_screen.place(x=0, y=0, relwidth=1, relheight=1)

Label(difficult_selection_screen, text="Escolha a dificuldade", font=(FONT_FAMILY, 24, "bold"), bg=BACKGROUND_COLOR, fg="white").pack(pady=40)



#Instancia a classe ScreenGame
def show_first_grade_screen():
    difficult_selection_screen.pack_forget()

    if qual_conjunto == "primeiro_ano":
        csv_path = "public/data/kanji_primeiro_ano.csv"
    elif qual_conjunto == "segundo_ano":
        csv_path = "public/data/kanji_segundo_ano.csv"
    elif qual_conjunto == "terceiro_ano":
        csv_path = "public/data/kanji_terceiro_ano.csv"

    game_screen = ScreenGame(window, initial_screen, csv_path)
    game_screen.first_grade_kanji_screen.pack(fill="both", expand=True)



Button(difficult_selection_screen, text="Normal", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=show_first_grade_screen).pack(pady=10)
Button(difficult_selection_screen, text="Difícil", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold")).pack(pady=10)
Button(difficult_selection_screen, text="Voltar", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=return_main_screen).pack(pady=10)

window.mainloop()
