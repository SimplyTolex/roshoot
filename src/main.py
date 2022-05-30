from tkinter import *
import random
from tkinter import filedialog

buttonList = []
questionsList = []
rightAnswer = ""
playerScore = 0
# FileValid = False     TODO: Disable button if file is invalid


class Question():
    def __init__(self, q, a):
        self.quest = q
        self.ans = a


obj1 = Question("кто такой форд", ["фокус", "это они а не я", "твое имя", "я"])
questionsList.append(obj1)

obj2 = Question("на чём написан РОСХУТ?", ["питон", "кобол"])
questionsList.append(obj2)


def button_creator(count):
    global errorLabel
    if count % 2 == 0:
        for i in range(count):
            currentButton = Button()
            # If button's number is odd, then we add 0 (0.5 * 0 = 0);
            # If, however, we add an even numbered button, then we will add 0,5 and the button will be shifted
            currentButton.place(rely=0.5 + ((0.5 / (count / 2)) * (i // 2)),
                                relx=0.05 + 0.5 * (i % 2),
                                relwidth=0.4,
                                relheight=0.5 / (count / 2) - 0.05)
            buttonList.append(currentButton)
    else:
        errorLabel.config(text="Unable to create odd number of buttons!")


def question_render(questionNumber, correct):
    global playerScore
    if correct:
        playerScore += 1
    if questionNumber < len(questionsList):
        global rightAnswer
        for i in buttonList:
            i.destroy()
        rightAnswer = questionsList[questionNumber].ans[0]
        buttonList.clear()
        answerCounter = len(questionsList[questionNumber].ans)
        button_creator(answerCounter)
        countFreeAnswer = answerCounter
        for i in range(answerCounter):
            answerText = questionsList[questionNumber].ans
            buttonList[i].config(text=answerText[random.randint(0, countFreeAnswer - 1)])
            questionsList[questionNumber].ans.remove(buttonList[i]['text'])
            countFreeAnswer -= 1
            # buttonList[i].config(command=lambda: question_render(questionNumber+1))
            if buttonList[i]["text"] == rightAnswer:
                buttonList[i].config(command=lambda: question_render(questionNumber + 1, True))
            else:
                buttonList[i].config(command=lambda: question_render(questionNumber + 1, False))
        questionLabel.config(text=questionsList[questionNumber].quest)
    else:
        for i in buttonList:
            i.destroy()
        questionLabel.config(text="Поздравляем!\nПравильных ответов:\n" + str(playerScore) + " / " + str(len(questionsList)))


def startGame():
    chooseFile.destroy()
    chosenFileLabel.destroy()
    startButton.destroy()
    question_render(0, False)


def openFile():
    global errorLabel
    f = open(filedialog.askopenfilename(), "r", encoding="utf-8")
    print(f)
    questionsList.clear()
    numberQuestion = -1
    questionFlag = False
    for l in f.readlines():
        if l[0] == "?":
            questionFlag = True
            numberQuestion += 1
            obj = Question(l[1:len(l)], [])
            questionsList.append(obj)
        elif not questionFlag:
            errorLabel.config(text="QuestionsFile Syntax Error: there is no question to add answer to!")
            print("hi")
        elif l[0] == "#":
            pass    # TODO: add comment functionality
        else:
            questionsList[numberQuestion].ans.append(l)
    chosenFileLabel.config(text="Выбран файл: " + str(f)[25:len(str(f))-28])
    f.close()


root = Tk()
root.geometry("640x480")
root.title("ROSHOOT? CLIENT v0.3")

questionLabel = Label(root, font=("Arial", "30"))
questionLabel.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.4)

chosenFile = "Выбраны стандартные вопросы (выберите свои с помощью кнопки сверху)"
errorLabel = Label(text="")
errorLabel.pack()

chooseFile = Button(root, text="Открыть файл с вопросами", command=openFile)
chooseFile.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.6)
chosenFileLabel = Label(root, text=chosenFile)
chosenFileLabel.place(relwidth=1, relheight=0.1, relx=0, rely=0.7)
startButton = Button(root, text="Начать викторину!", command=startGame)
startButton.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)

root.mainloop()
