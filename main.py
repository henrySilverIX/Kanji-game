import pandas as pd # type: ignore
from tkinter import *
import pygame
import sys
import os


BACKGROUND_COLOR = "#494949"
FONT_FAMILY = "Ariel"

base_path = os.path.dirname(__file__)


# Inicializa o mixer de som
pygame.mixer.init()

# Função para encontrar arquivos corretamente
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Executável
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Script normal
        return os.path.join(os.path.abspath("."), relative_path)

#Screen Configuration - Main screen
window = Tk()
window.title("Quiz Kanji")
window.minsize(width=1920, height=1080)


#First Screen
initial_screen = Frame(window)
initial_screen.pack(fill="both", expand=True)

#Button Functions - First Screen
def go_to_difficult_level():
    initial_screen.pack_forget() #hide the current screen
    difficult_selection_screen.pack(fill="both", expand=True)


# Background main screen configuration - First Screen
background_image = PhotoImage(file=resource_path("public/img/background.png"))
background_label = Label(initial_screen, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Labels - First Screen
Label(initial_screen, text="Quiz de Japonês - Kanji!", font=(FONT_FAMILY, 24, "bold"), bg=BACKGROUND_COLOR, fg="white").pack(pady=40)

#Buttons - First Screen
kanji_primeiro_ano_button = Button(initial_screen, text="1º ano", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=go_to_difficult_level)
kanji_primeiro_ano_button.pack(pady=10)

kanji_primeiro_segundo_button = Button(initial_screen, text="2º ano", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=go_to_difficult_level)
kanji_primeiro_segundo_button.pack(pady=10)


#Difficult Level Screen
difficult_selection_screen = Frame(window)

#Button Functions - First Screen
def return_main_screen():
    difficult_selection_screen.pack_forget() #hide the current screen
    initial_screen.pack(fill="both", expand=True)

def first_grade_kanji_screen_selection_level():
    difficult_selection_screen.pack_forget() #hide the current screen
    first_grade_kanji_screen.pack(fill="both", expand=True)


# Background main screen configuration - Difficult Level Screen
background_image_difficult_screen = PhotoImage(file=resource_path("public/img/background2.png"))
background_label_difficult_screen = Label(difficult_selection_screen, image=background_image_difficult_screen)
background_label_difficult_screen.place(x=0, y=0, relwidth=1, relheight=1)

#Labels - Difficult Level Screen
Label(difficult_selection_screen, text="Escolha a dificuldade", font=(FONT_FAMILY, 24, "bold"), bg=BACKGROUND_COLOR, fg="white").pack(pady=40)

#Buttons - Difficult Level Screen
normal_difficulty = Button(difficult_selection_screen, text="Normal", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=first_grade_kanji_screen_selection_level)
normal_difficulty.pack(pady=10)

hard_difficulty = Button(difficult_selection_screen, text="Difícil", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"))
hard_difficulty.pack(pady=10)

return_button = Button(difficult_selection_screen, text="Voltar", width=15, bg="#f5be6c", font=(FONT_FAMILY, 12, "bold"), command=return_main_screen)
return_button.pack(pady=10)


#First Grade Kanji
first_grade_kanji_screen = Frame(window)

#Button Functions - First Grade Kanji
def return_main_screen():
    first_grade_kanji_screen.pack_forget() #hide the current screen
    initial_screen.pack(fill="both", expand=True)

# Background main screen configuration - First Grade Kanji
background_image_first_grade_kanji_screen = PhotoImage(file=resource_path("public/img/background3.png"))
background_label_first_grade_kanji_screen = Label(first_grade_kanji_screen, image=background_image_first_grade_kanji_screen)
background_label_first_grade_kanji_screen.place(x=0, y=0, relwidth=1, relheight=1)

#Loading the csv file with kanji
csv_path = os.path.join(base_path, 'public', 'data', 'kanji_primeiro_ano.csv')
first_grade_kanji = pd.read_csv(csv_path)



#Label for the question - First Grade Kanji
random_line = first_grade_kanji.sample().iloc[0]
kanji_atual = random_line["Kanji"]
question_first_grade_kanji = Label(first_grade_kanji_screen, text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}", font=(FONT_FAMILY, 16, "bold"), width=15, height=4)
question_first_grade_kanji.pack(pady=40)



# Inner Frame for the buttons with the kanji
kanji_buttons_frame = Frame(first_grade_kanji_screen, bg=BACKGROUND_COLOR)
kanji_buttons_frame.pack(pady=20)

indice_atual = random_line.name


def new_question():
    global kanji_atual, indice_atual

    random_line = first_grade_kanji.sample().iloc[0]
    kanji_atual = random_line["Kanji"]
    indice_atual = random_line.name  # 👈 salva o índice globalmente
    question_first_grade_kanji.config(text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}")


def check_answer(kanji_clicado, botao):
    if kanji_clicado == kanji_atual:
        pygame.mixer.music.load("public/audio/right_answer_aud.mp3")  # file path
        pygame.mixer.music.play()
        botao.config(bg="green")

        #Drop the kanji from the dataframe
        first_grade_kanji.drop(index=indice_atual, inplace=True)

        window.after(800, new_question)
    
    else:
        pygame.mixer.music.load("public/audio/wrong_answer_aud.mp3")  # file path
        pygame.mixer.music.play()
        botao.config(bg="red")
        window.after(800, new_question)

            

# Número de colunas por linha
COLUNAS = 10

for i, kanji in enumerate(first_grade_kanji["Kanji"].to_list()):
    linha = i // COLUNAS
    coluna = i % COLUNAS
    kanji_button = Button(
        kanji_buttons_frame,
        text=kanji,
        width=4,
        height=2,
        bg="#f5be6c",
        font=(FONT_FAMILY, 18, "bold"),
    )
    kanji_button.config(command=lambda k=kanji, b=kanji_button: check_answer(k, b))
    kanji_button.grid(row=linha, column=coluna, padx=5, pady=5)

window.mainloop()