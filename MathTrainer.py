from tkinter import *
import random

symbol = None
complexity = None
difficulty = None
eventLabelText = None
saved = False

class Page(Frame):
    def __init__(self, *Args, **kwargs):
        Frame.__init__(self, *Args, **kwargs)

    def show(self):
        self.lift()

class Options(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        symbolVar = StringVar()
        complexityVar = IntVar()
        difficultyVar = StringVar()

        symbolLabel = Label(self, text="Symbol: ")
        symbolEntry = Entry(self, textvariable=symbolVar)
        symbolVar.set("all")

        complexityLabel = Label(self, text="Complexity: ")
        complexityEntry = Entry(self, textvariable=complexityVar)
        complexityVar.set("2")

        difficultyLabel = Label(self, text="Difficulty: ")
        difficultyList = ["I’m Too Young to Die", "Hurt Me Plenty", "Ultra Violence", "Nightmare"]
        difficultyVar.set("Choose a Difficulty")
        difficultyMenu = OptionMenu(self, difficultyVar, *difficultyList)

        def Submit():
            global complexity, symbol, difficulty, eventLabelText, saved

            if(symbolVar.get() != "all" and symbolVar.get() != "+" and symbolVar.get() != "-" and symbolVar.get() != "*"):
                symbolVar.set("all")

            if(complexityVar.get() < 2):
                complexityVar.set(2)

            if(difficultyVar.get() == "Choose a Difficulty"):
                difficultyVar.set("I’m Too Young to Die")

            if(difficultyVar.get() == "I’m Too Young to Die"):
                difficulty = 25
            elif(difficultyVar.get() == "Hurt Me Plenty"):
                difficulty = 20
            elif(difficultyVar.get() == "Ultra Violence"):
                difficulty = 15
            else:
                difficulty = 10
            
            symbol = symbolVar.get()
            complexity = complexityVar.get()

            eventLabelText = str(complexity) + ", " + symbol + ", " + difficultyVar.get()
            eventLabelTextVar.set(eventLabelText)
            timeLabelTextVar.set(difficulty)

            saved = True

        saveButton = Button(self, text="Save", command=Submit)

        complexityLabel.grid(row=1, column=1)
        complexityEntry.grid(row=1, column=2)
        symbolLabel.grid(row=2, column=1)
        symbolEntry.grid(row=2, column=2)
        difficultyLabel.grid(row=3, column=1)
        difficultyMenu.grid(row=3, column=2)
        saveButton.grid(row=4, column=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
class Game(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        eventLabel = Label(self, textvariable=eventLabelTextVar)
        timerLabel = Label(self, text="Time Remaining: ")
        timeLabel = Label(self, textvariable=timeLabelTextVar)
        scoreTextLabel = Label(self, text="Score: ")
        scoreLabel = Label(self, textvariable=scoreVar)
        equationLabel = Label(self, textvariable=equationLabelVar)
        answerEntry = Entry(self, textvariable=answerVar)

        answerEntry.delete(0)

        def CheckSaved():
            global saved

            if(saved):
                startButton['state'] = 'normal'
                saved = False
            self.after(100, CheckSaved)

        def StartGame():
            startButton['state'] = 'disabled'
            eventLabelTextVar.set(eventLabelText)
            timeLabelTextVar.set(difficulty + 1)
            scoreVar.set(0)
            Timer()
            EquationCreator()

        def Timer():
            if(timeLabelTextVar.get() <= 0):
                timeLabelTextVar.set(0)
                equationLabelVar.set("You Lose!")
                startButton['state'] = 'normal'
            else:
                timeLabelTextVar.set(timeLabelTextVar.get() - 1)
                self.after(1000, Timer)

        answer = None

        def EquationCreator():
            global answer
            symbols = ["all", "+", "-", "*"]
            numbers = [random.randint(0, 10) for i in range(complexity)]
            equation = str(numbers[0])

            if(symbol == "all"):
                symbolIndexArr = [symbols[random.randint(1, 3)] for i in range(complexity - 1)]
                
                counter = 1
                for x in symbolIndexArr:
                    equation += " " + x + " " + str(numbers[counter])
                    counter += 1
            else:
                counter = 1
                for x in range(len(numbers)):
                    equation += " " + x + " " + str(numbers([counter]))
                    counter += 1

            answer = eval(equation)

            equation += " = "
            equationLabelVar.set(equation)

        def ChangeRedColor():
            currentColor = answerEntry.cget("background")

            if(currentColor == "white"):
                answerEntry.config(background="red")
                self.after(500, ChangeRedColor)
            else:
                answerEntry.config(background="white")

        def ChangeGreenColor():
            currentColor = answerEntry.cget("background")

            if(currentColor == "white"):
                answerEntry.config(background="green")
                self.after(500, ChangeGreenColor)
            else:
                answerEntry.config(background="white")

        def Enter(event):
            global answer
            try:
                if(answerVar.get() == answer):
                    scoreVar.set(scoreVar.get() + 1)
                    answerVar.set(0)
                    ChangeGreenColor()
                    EquationCreator()
                    timeLabelTextVar.set(difficulty)
                    answerEntry.delete(0)
                else:
                    ChangeRedColor()
            except:
                ChangeRedColor()
            
        answerEntry.bind('<Return>', Enter)

        startButton = Button(self, text="Start", command=StartGame)
        startButton['state'] = 'disabled'
        CheckSaved()

        eventLabel.grid(row=1, column=1)
        timerLabel.grid(row=2, column=1)
        timeLabel.grid(row=2, column=2)
        scoreTextLabel.grid(row=3, column=1)
        scoreLabel.grid(row=3, column=2)
        equationLabel.grid(row=4, column=1)
        answerEntry.grid(row=5, column=1)
        startButton.grid(row=6, column=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Options(self)
        p2 = Game(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Options", command=p1.show)
        b2 = Button(buttonframe, text="Game", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = Tk()
    root.title("Math Trainer")

    eventLabelTextVar = StringVar()
    timeLabelTextVar = IntVar()
    equationLabelVar = StringVar()
    answerVar = IntVar()
    scoreVar = IntVar()

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("500x500")
    root.mainloop()