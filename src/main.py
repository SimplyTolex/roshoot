# ROSHOOT? -- an open-source Python application for holding a quiz or trivia.
# Copyright (C) 2022  SimplyTolex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# imports
from tkinter import *
import random
from tkinter import filedialog
import yaml


# setting up global vars
button_list = []
questions_list = []
right_answer = ""
player_score = 0


# reading config.yaml
with open('cfg/config.yaml', 'r') as yaml_file:
    cfg = yaml.safe_load(yaml_file)


class Question():
    def __init__(self, self_quest, self_ans):
        self.quest = self_quest
        self.ans = self_ans


def button_creator(count):
    global error_label

    if count % 2 == 0:
        for i in range(count):
            current_button = Button()
            # If button's number is odd, then we add 0 (0.5 * 0 = 0);
            # If, however, we add an even numbered button,
            # then we will add 0,5 and the button will be shifted
            current_button.place(rely=0.5 + ((0.5 / (count / 2)) * (i // 2)), relx=0.05 +
                                 0.5 * (i % 2), relwidth=0.4, relheight=0.5 / (count / 2) - 0.05)
            button_list.append(current_button)
    else:       # TODO: make odd number of answers look pretty
        error_label.config(text="Unable to create odd number of buttons!")


def question_render(current_question, is_answer_correct):

    global player_score
    global back_to_title_button

    if is_answer_correct:
        player_score += 1

    # checks if we still have question to show
    if current_question < len(questions_list):

        global right_answer

        for i in button_list:
            i.destroy()       # destroy buttons from previous questions to stop them from piling up

        right_answer = questions_list[current_question].ans[0]
        button_list.clear()
        # get how many answers a question has...
        answer_count = len(questions_list[current_question].ans)
        # ... to create just enough buttons for them
        button_creator(answer_count)

        buttons_to_fill_left = answer_count
        for i in range(answer_count):
            answer_text = questions_list[current_question].ans
            button_list[i].config(
                text=answer_text[random.randint(0, buttons_to_fill_left - 1)])
            questions_list[current_question].ans.remove(button_list[i]['text'])
            buttons_to_fill_left -= 1
            # check if the i button happend to have a right answer
            if button_list[i]["text"] == right_answer:
                button_list[i].config(
                    command=lambda: question_render(current_question + 1, True))
            else:
                button_list[i].config(command=lambda: question_render(
                    current_question + 1, False))
        # set the question
        question_label.config(text=questions_list[current_question].quest)
    else:       # if we ran out of questions, destroy everyting and show the so called 'end screen'
        for i in button_list:
            i.destroy()
        question_label.config(
            text=f"Поздравляем!\nПравильных ответов:\n {player_score} / {len(questions_list)}")
        # TODO: stuff gets destroyed and therefore doesn't work anymore:
        # If you remove these lines below (just like they are right now), everything will work fine. There is something with these lines that breaks everything, probably the () in the command, as they are wacky in tk.
        # back_to_title_button = Button(text="Назад в главное меню", command=load_main_menu(True))
        # back_to_title_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)


def start_game(repeat_flag):
    global choose_file_button
    global chosen_file_label
    global start_button
    global back_to_title_button

    choose_file_button.destroy()
    chosen_file_label.destroy()
    start_button.destroy()
    if repeat_flag:
        back_to_title_button.destroy()
    # send False to question_render so it won't trigger anything
    question_render(0, False)


def file_manager():
    global error_label

    # TODO: if the user open the dialog, then choses nothing (by just closing the window), the app will throw an error
    f = open(filedialog.askopenfilename(), "r", encoding="utf-8")
    questions_list.clear()
    question_number = -1
    question_flag = False

    for currentLine in f.readlines():
        if currentLine[0] == "?":   # if this line is a question
            # set the flag so it will not trigger on the next line (which should be the answer)
            question_flag = True
            question_number += 1
            question_to_append = Question(currentLine[1:len(currentLine)], [])
            questions_list.append(question_to_append)
        elif not question_flag:
            error_label.config(
                text="QuestionFile Syntax Error: there is no question to add answer to!")
        elif currentLine[0] == "#":     # if this line is comment
            pass    # TODO: add comment functionality
            # Actually, the better goal will be to make use of some already well defined format like yaml or ini or something else

        else:       # if this line is answer
            questions_list[question_number].ans.append(currentLine)
    f.close()

    if question_flag:
        chosen_file_label.config(
            text="Выбран файл: " + str(f)[25:len(str(f))-28])
        start_button.config(text="Начать викторину!", state=NORMAL)
    else:
        chosen_file_label.config(text="Выбран недействительный файл")


def load_main_menu(repeat_flag):
    global question_label
    global chosen_file
    global choose_file_button
    global chosen_file_label
    global start_button

    question_label = Label(root, font=("Arial", "30"))
    question_label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.4)

    chosen_file = "Выберете файл, чтобы начать викторину!"
    choose_file_button = Button(
        root, text="Открыть файл с вопросами", command=file_manager)
    choose_file_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.6)

    chosen_file_label = Label(root, text=chosen_file)
    chosen_file_label.place(relwidth=1, relheight=0.1, relx=0, rely=0.7)

    if repeat_flag:
        start_button = Button(root, text="Сперва выберете файл...", command=(
            lambda: start_game(True)), state=DISABLED)
        start_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)
    else:
        start_button = Button(root, text="Сперва выберете файл...", command=(
            lambda: start_game(False)), state=DISABLED)
        start_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)


def test_moment():
    print("Test moment")


# Creating main window
root = Tk()
root.geometry("640x480")
root.title(f"ROSHOOT? CLIENT v{cfg['program']['version']}")
root.option_add('*tearOff', FALSE)  # prevents "tear-off" in menubar


# menubar Time
menubar = Menu(root)
root['menu'] = menubar
root.config(menu=menubar)

menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menu_help = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Файл', underline=0)
menubar.add_cascade(menu=menu_edit, label='Изменить', underline=0)
menubar.add_cascade(menu=menu_help, label='Помощь', underline=0)

## setting up file menu
menu_file.add_command(label="Открыть файл...")
menu_file.add_separator()
menu_file.add_command(label="Пропустить вопрос")
menu_file.add_command(label="Начать викторину с начала")
menu_file.add_command(label="Закончить викторину")
menu_file.add_separator()
menu_file.add_command(label="Выйти", command=exit)

## setting up edit menu
menu_edit.add_command(label="Настройки...", underline=0)

## setting up help menu
menu_help.add_command(label="О программе...")

# setting up error output
error_label = Label(text="")
error_label.pack()


# start the main loop
load_main_menu(False)
root.mainloop()
