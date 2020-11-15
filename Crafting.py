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
    def __init__(self,attribute,ability,stunt=0,supremeMasterworkFocusActive=True):
        self.attribute = attribute
        self.ability = ability
        self.dice = attribute+ability+self.stunt_reward(stunt)[0]
        self.dice_pool = []
        self.supremeMasterworkFocusActive=supremeMasterworkFocusActive

    def scenario(self):
        #Temporary function to run a potential roll
        #Roll Initial Pool
        self.dice_pool = self.roll(self.dice)

        #Roll extra dice with Experiential Conjuring of True Void

        #Reroll 10s and 6s with Flawless Handiwork Method.

        #If ECoTV is active, with 3 of a kind successes, chose one non success die and convert to a 10

        #Apply Divine inspiration technique - recursively gain additional non charm dice

        #Key off DIT roll with Holistic Miracle Understanding

        #Double 9s or 8s with Supreme Masterwork Focus
        if self.supremeMasterworkFocusActive:
            self.supremeMasterworkFocus(advanced=True)

    def stunt_reward(self,stunt_num):
        def zero():
            return [0,0,0]
        def one():
            #return 2 dice, 0 auto success, 0 willpower
            return [2,0,0]
        def two():
            return [2,1,1]
        def three():
            return [2,2,2]

        options = {0 : zero(),
                   1 : one(),
                   2 : two(),
                   3 : three()
        }
        return options[stunt_num]

    #Roll x number of dice and store to list
    def roll(self,ndice):
        #roll the dice
        dice_results=[random.randint(1, 10) for i in range(0, ndice)]
        #list concatentation
        self.dice_pool += dice_results

    def success(self):
        #Detect number of successes. Create list of 1 or 2 depending on 10 status
        self.successes = [(1 if (i>=7 and i<10) else (2 if i==10 else 0)) for i in self.dice_pool]
        return self.successes

    def total_succ(self):
        return sum(self.successes)

    def supremeMasterworkFocus(self, advanced=False):
        if advanced:
            #Double 8s (Basic, major or superior Project; 5m, 1WP, 1GXP)
            self.successes = [2 if (i >= 8) else 0 for i in self.dice_pool]
            return self.successes

        else:
            #Double 9s (basic and major projects; 6m)
            self.successes=[2 if i>=9 else 0 for i in self.dice_pool]
            return self.successes

    def flawlessHandiworkMethod(self):
        return

    def experientialConjuringofTrueVoid(self):
        return

    def firstMovementoftheDemiurge(self):
        return

    def divineInspirationTechnique(self):
        return

    def holisticMiracleUnderstanding(self):
        return


fang=crafter(5,5)
print(fang.dice_pool)
fang.success()