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


from tkinter import *
import random
from tkinter import filedialog

button_list = []
questions_list = []
right_answer = ""
player_score = 0
# FileValid = False     TODO: Disable button if file is invalid


class Question():
    def __init__(self, self_quest, self_ans):
        self.quest = self_quest
        self.ans = self_ans


default_question_1 = Question("кто такой форд", ["фокус", "это они а не я", "твое имя", "я"])
questions_list.append(default_question_1)

default_question_2 = Question("на чём написан РОСХУТ?", ["питон", "кобол"])
questions_list.append(default_question_2)


def button_creator(count):
    global error_label
    if count % 2 == 0:
        for i in range(count):
            current_button = Button()
            # If button's number is odd, then we add 0 (0.5 * 0 = 0);
            # If, however, we add an even numbered button,
            # then we will add 0,5 and the button will be shifted
            current_button.place(rely=0.5 + ((0.5 / (count / 2)) * (i // 2)),
                                 relx=0.05 + 0.5 * (i % 2),
                                 relwidth=0.4,
                                 relheight=0.5 / (count / 2) - 0.05)
            button_list.append(current_button)
    else:       # TODO: make odd number of answers look pretty
        error_label.config(text="Unable to create odd number of buttons!")


def question_render(current_question, is_answer_correct):

    global player_score

    if is_answer_correct:
        player_score += 1

    if current_question < len(questions_list):      # checks if we still have question to show

        global right_answer

        for i in button_list:
            i.destroy()       # destroy buttons from previous questions to stop them from piling up

        right_answer = questions_list[current_question].ans[0]
        button_list.clear()
        answer_count = len(questions_list[current_question].ans)        # get how many answers a question has...
        button_creator(answer_count)                                    # ... to create just enough buttons for them

        buttons_to_fill_left = answer_count
        for i in range(answer_count):
            answer_text = questions_list[current_question].ans
            button_list[i].config(text=answer_text[random.randint(0, buttons_to_fill_left - 1)])
            questions_list[current_question].ans.remove(button_list[i]['text'])
            buttons_to_fill_left -= 1
            if button_list[i]["text"] == right_answer:      # check if the i button happend to have a right answer
                button_list[i].config(command=lambda: question_render(current_question + 1, True))
            else:
                button_list[i].config(command=lambda: question_render(current_question + 1, False))
        question_label.config(text=questions_list[current_question].quest)      # set the question
    else:       # if we ran out of questions, destroy everyting and show the so called 'end screen'
        for i in button_list:
            i.destroy()
        question_label.config(text="Поздравляем!\nПравильных ответов:\n" + str(player_score) + " / " + str(len(questions_list)))        # TODO: make it fString instead to reduce clutter


def start_game():
    choose_file_button.destroy()
    chosen_file_label.destroy()
    start_button.destroy()
    question_render(0, False)   # send False to question_render so it won't trigger anything


def file_manager():
    global error_label
    f = open(filedialog.askopenfilename(), "r", encoding="utf-8")
    # print(f)      # sends filepath to debug console
    questions_list.clear()
    question_number = -1
    question_flag = False

    for currentLine in f.readlines():
        if currentLine[0] == "?":   # if this line is a question
            question_flag = True     # set the flag so it will not trigger on the next line (which should be the answer)
            question_number += 1
            question_to_append = Question(currentLine[1:len(currentLine)], [])
            questions_list.append(question_to_append)
        elif not question_flag:
            error_label.config(text="QuestionsFile Syntax Error: there is no question to add answer to!")
        elif currentLine[0] == "#":     # if this line is comment
            pass    # TODO: add comment functionality
        else:       # if this line is answer
            questions_list[question_number].ans.append(currentLine)
    chosen_file_label.config(text="Выбран файл: " + str(f)[25:len(str(f))-28])
    f.close()


root = Tk()
root.geometry("640x480")
root.title("ROSHOOT? CLIENT v0.3")      # TODO: move version number into conf file (that doesn't exist yet)

error_label = Label(text="")
error_label.pack()

question_label = Label(root, font=("Arial", "30"))
question_label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.4)

chosen_file = "Выбраны стандартные вопросы (выберите свои с помощью кнопки сверху)"
choose_file_button = Button(root, text="Открыть файл с вопросами", command=file_manager)
choose_file_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.6)

chosen_file_label = Label(root, text=chosen_file)
chosen_file_label.place(relwidth=1, relheight=0.1, relx=0, rely=0.7)

start_button = Button(root, text="Начать викторину!", command=start_game)
start_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)

root.mainloop()
