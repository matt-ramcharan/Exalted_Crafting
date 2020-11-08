import random
import PySimpleGUI as sg
# from itertools import chain

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()


class crafter:
    def __init__(self,attribute,ability):
        self.attribute = attribute
        self.ability = ability
        self.dice = attribute+ability

    #Roll x number of dice and store to list
    def roll(self):
        #roll the dice
        self.dice_results=[random.randint(1, 10) for i in range(0, self.dice)]
        return self.dice_results

    def success(self):
        #Detect number of successes. Create list of 1 or 2 depending on 10 status
        self.successes = [(1 if (i>=7 and i<10) else (2 if i==10 else 0)) for i in self.dice_results]
        return self.successes

    def total_succ(self):
        return sum(self.successes)

    def supremeMasterworkFocus(self, advanced=False):
        if advanced:
            #Double 9s (basic and major projects; 6m)
            self.successes=[2 if i==9 else i for i in self.dice_results]

        else:
            #Double 8s (Basic, major or superior Project; 5m, 1WP, 1GXP)
            self.successes = [2 if (i == 8 or i == 9) else i for i in self.dice_results]


fang=crafter(5,5)
fang.roll()
print(fang.dice_results)
fang.success()