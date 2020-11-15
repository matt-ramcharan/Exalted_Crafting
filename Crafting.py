import random
import PySimpleGUI as sg
# from itertools import chain
from collections import Counter

# sg.theme('DarkAmber')   # Add a touch of color
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]
#
# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])
#
# window.close()


class crafter:
    def __init__(self,attribute,ability,essence=3,int=4,stunt=0,supremeMasterworkFocusActive=True):
        self.attribute = attribute
        self.ability = ability
        self.dice = attribute+ability
        self.dice_pool = []
        self.supremeMasterworkFocusActive=supremeMasterworkFocusActive
        self.essence=essence
        self.int=int
        self.autosucc=0

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

        self.roll(options[stunt_num][0])
        self.autosucc+=options[stunt_num][1]

    #Roll x number of dice and store to list
    def roll(self,ndice):
        #roll the dice
        dice_results=[diceresult(random.randint(1, 10)) for i in range(0, ndice)]
        #list concatentation
        self.dice_pool += dice_results

    def success(self):
        #Detect number of successes. Create list of 1 or 2 depending on 10 status
        self.successes = [(1 if (i.result>=7 and i.result<10) else (2 if i.result==10 else 0)) for i in self.dice_pool]
        return self.successes

    def total_succ(self):
        return sum(self.successes)

    def supremeMasterworkFocus(self, advanced=False):
        if advanced:
            #Double 8s (Basic, major or superior Project; 5m, 1WP, 1GXP)
            self.successes = [2 if (i.result >= 8) else 0 for i in self.dice_pool]
            return self.successes

        else:
            #Double 9s (basic and major projects; 6m)
            self.successes=[2 if i.result>=9 else 0 for i in self.dice_pool]
            return self.successes

    def flawlessHandiworkMethod(self):
        new_tens = sum([1 if (res.tenreroll==False and res.result==10) else 0 for res in self.dice_pool])
        for die in self.dice_pool:
            if (die.result==10 and die.tenreroll==False):
                die.tenreroll=True
        self.roll(new_tens)

        new_sixes = sum([1 if (res.sixreroll==False and res.result==6) else 0 for res in self.dice_pool])
        for die in self.dice_pool:
            if (die.result==6 and die.sixreroll==False):
                die.sixreroll=True
        self.roll(new_sixes)

    def experientialConjuringofTrueVoid(self):
        self.roll(self.int+self.essence)
        self.autosucc += 1


    def firstMovementoftheDemiurge(self,ECoTV):
        #FMotD enhances the prerequisite, so EcoTV must be active
        if ECoTV==True:
            success_res=[res.result for res in self.dice_pool if (res.result>=7 and res.FmoDThree==False)]
            success_counts = Counter(success_res)
            total_ten_changes=sum([success_counts[7] // 3,
                                    success_counts[8] // 3,
                                    success_counts[9] // 3,
                                    success_counts[10] // 3])

            #Add FmoDThree tag to dice used to convert non succ to 10s
            for i in success_counts:
                for j in range(0,success_counts[i]//3):
                    for die in self.dice_pool:
                        if die.result==i:
                            die.FmoDThree=True
            #Convert non succ to 10s
            for die in self.dice_pool:
                if die.result<7:
                    if total_ten_changes>0:
                        die.result=10
                        total_ten_changes-=1

    def divineInspirationTechnique(self):
        return

    def holisticMiracleUnderstanding(self):
        return

class diceresult:
    def __init__(self,die):
        self.result=die
        self.tenreroll=False
        self.sixreroll=False
        self.FmoDThree=False
        self.DITThree=False

#Return list of dice results from list of objects
#[dice_pool.result for dice_pool in fang.dice_pool]

fang=crafter(5,5)
print(fang.dice_pool)
fang.success()

fang.dice_pool=[diceresult(1),diceresult(1),diceresult(1),diceresult(1),diceresult(9),diceresult(9),diceresult(9)]
fang.firstMovementoftheDemiurge(True)
[dice_pool.result for dice_pool in fang.dice_pool]
[dice_pool.FmoDThree for dice_pool in fang.dice_pool]