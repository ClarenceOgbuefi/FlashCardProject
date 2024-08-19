import random
from tkinter import *
from random import *
import pandas
from csv import DictWriter

BACKGROUND_COLOR = "#B1DDC6"
word = {}
to_learn = {}
learned = {}

# Data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/igbo_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient = "records")


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = choice(to_learn)
    canvas.itemconfig(face, image=flashcard_front_img)
    canvas.itemconfig(card_word, text = word["Igbo"], fill="black")
    canvas.itemconfig(card_title, text="Igbo", fill="black")
    flip_timer = window.after(5000, func=flip)


def flip():
    canvas.itemconfig(face, image=flashcard_back_img)
    canvas.itemconfig(card_word, text = word["English"], fill="white")
    canvas.itemconfig(card_title, text="English", fill="white")


def is_known():
    to_learn.remove(word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index = False)
    learned.update(word)
    field_names = ["Igbo", "English"]
    with open("data/learned_words.csv", "a") as bank:
        dictwriter = DictWriter(bank, fieldnames=field_names)
        dictwriter.writerow(word)
        bank.close()
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Flashy")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)
flashcard_back_img = PhotoImage(file = "images/card_back.png")
flashcard_front_img = PhotoImage(file = "images/card_front.png")

flip_timer = window.after(5000, func=flip)

# Canvas
canvas = Canvas(width = 800, height = 526)
face = canvas.create_image(400, 263, image = flashcard_front_img)
card_title = canvas.create_text(400, 150, text = "Title", font=("Arial", 40, "italic"), fill = "black")
card_word = canvas.create_text(400, 263, text = "word", font=("Arial", 40, "bold"), fill = "black")
canvas.config(bg = BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column = 0, row = 0, columnspan = 2)


# Button
x_mark = PhotoImage(file = "images/wrong.png")
x_button = Button(image = x_mark, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
x_button.grid(column = 0, row = 1)

checkmark = PhotoImage(file = "images/right.png")
check_button = Button(image = checkmark, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=is_known)
check_button.grid(column = 1, row = 1)

next_card()

window.mainloop()