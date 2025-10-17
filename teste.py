import pandas as pd # type: ignore
import sys
import os



base_path = os.path.dirname(__file__)



#Loading the csv file with kanji
csv_path = os.path.join(base_path, '..', 'public', 'data', 'kanji_primeiro_ano.csv')


def new_question():
    global kanji_atual, indice_atual
    if first_grade_kanji.empty:
        question_first_grade_kanji.config(
            text="Parabéns! Você completou todos os kanji 🎉",
            fg="lightgreen"
        )
        for child in kanji_buttons_frame.winfo_children():
            child.config(state=DISABLED)
        return

    random_line = first_grade_kanji.sample().iloc[0]
    kanji_atual = random_line["Kanji"]
    indice_atual = random_line.name  # 👈 salva o índice globalmente
    question_first_grade_kanji.config(
        text=f"{random_line['Português']}\n{random_line['On']}\n{random_line['Kun']}"
    )
