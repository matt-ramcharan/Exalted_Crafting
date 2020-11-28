import random
import PySimpleGUI as sg
# from itertools import chain
from collections import Counter
import numpy as np

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
    def __init__(self,attribute,ability,essence=3,int=4,stunt=0,supremeMasterworkFocusActive=False,SMFAdvanced=False):
        self.attribute = attribute
        self.ability = ability
        self.dice = attribute+ability
        self.dice_pool = []
        self.supremeMasterworkFocusActive=supremeMasterworkFocusActive
        self.SMFAdvanced=SMFAdvanced
        self.essence=essence
        self.int=int
        self.autosucc=0
        self.HMUUsed=False

    # def scenario_enclosed(self):
    #
    #     #Temporary function to run a potential roll
    #     #Roll Initial Pool - ONCE
    #     self.roll(self.dice)
    #
    #     #Roll extra dice with Experiential Conjuring of True Void - ONCE
    #     self.experientialConjuringofTrueVoid()
    #
    #     while True:
    #         #Reroll 10s and 6s with Flawless Handiwork Method.
    #         self.flawlessHandiworkMethod()
    #
    #         #If ECoTV is active, with 3 of a kind successes, chose one non success die and convert to a 10
    #         self.firstMovementoftheDemiurge(True)
    #
    #         #Apply Divine inspiration technique - recursively gain additional non charm dice
    #         self.divineInspirationTechnique()
    #
    #         #Double 9s or 8s with Supreme Masterwork Focus
    #         if self.supremeMasterworkFocusActive:
    #             self.supremeMasterworkFocus()

    def scenario(self):
        #Temporary function to run a potential roll
        #Roll Initial Pool
        self.roll(self.dice)
        print("First Roll!")

        #Roll extra dice with Experiential Conjuring of True Void
        self.experientialConjuringofTrueVoid()

        #Reroll 10s and 6s with Flawless Handiwork Method.
        self.flawlessHandiworkMethod()

        #Apply Divine inspiration technique - recursively gain additional non charm dice
        self.divineInspirationTechnique()

        #If ECoTV is active, with 3 of a kind successes, chose one non success die and convert to a 10
        self.firstMovementoftheDemiurge(True)


        #Double 9s or 8s with Supreme Masterwork Focus
        if self.supremeMasterworkFocusActive:
            self.supremeMasterworkFocus()



    def scenario_recur(self):

        #Reroll 10s and 6s with Flawless Handiwork Method.
        self.flawlessHandiworkMethod()

        #Apply Divine inspiration technique - recursively gain additional non charm dice
        self.divineInspirationTechnique()

        #If ECoTV is active, with 3 of a kind successes, chose one non success die and convert to a 10
        self.firstMovementoftheDemiurge(True)

        #Double 9s or 8s with Supreme Masterwork Focus
        if self.supremeMasterworkFocusActive:
            self.supremeMasterworkFocus()

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
        self.successes = [([1,i] if (i.result>=7 and i.result<10) else ([2,i] if i.result==10 else [0,i])) for i in self.dice_pool]
        return self.successes

    def total_succ(self):
        return sum(Extract(self.successes,0))

    def total_no_DIT_succ(self):
        all_successes=Extract(self.successes, 0)
        unused_successes=[]
        for index,element in enumerate(Extract(self.successes,1)):
            if element.DITThree==False:
                unused_successes.append(index)
        return(sum(np.array(all_successes)[unused_successes]))

    def supremeMasterworkFocus(self):
        if self.SMFAdvanced:
            #Double 8s (Basic, major or superior Project; 5m, 1WP, 1GXP)
            self.successes = [[2,i] if (i.result >= 8) else [0,i] for i in self.dice_pool]
            return self.successes

        else:
            #Double 9s (basic and major projects; 6m)
            self.successes=[[2,i] if i.result>=9 else [0,i] for i in self.dice_pool]
            return self.successes

    def flawlessHandiworkMethod(self):
        new_tens = sum([1 if (res.tenreroll==False and res.result==10) else 0 for res in self.dice_pool])
        for die in self.dice_pool:
            if (die.result==10 and die.tenreroll==False):
                die.tenreroll=True
        self.roll(new_tens)
        print("New from Tens")

        new_sixes = sum([1 if (res.sixreroll==False and res.result==6) else 0 for res in self.dice_pool])
        for die in self.dice_pool:
            if (die.result==6 and die.sixreroll==False):
                die.sixreroll=True
        self.roll(new_sixes)
        print("New from Sixes")


    def experientialConjuringofTrueVoid(self):
        self.roll(self.int+self.essence)
        print("Experiential!")
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
                conversion_num=success_counts[i]//3*3

                true_vals=np.array([dice_pool.result for dice_pool in self.dice_pool]) == i
                true_indices=[taggingIter for taggingIter, val in enumerate(true_vals) if val]
                for j in true_indices[:conversion_num]:
                    self.dice_pool[j].FmoDThree=True


                # for j in range(0,conversion_num):
                #
                #     if self.dice_pool[j].result==i:
                #         self.dice_pool[j].FmoDThree=True
                #     np.array([dice_pool.result for dice_pool in self.dice_pool]) == i

            #Convert non succ to 10s
            for die in self.dice_pool:
                if die.result<7:
                    if total_ten_changes>0:
                        die.result=10
                        total_ten_changes-=1

    def divineInspirationTechnique(self):
        if self.supremeMasterworkFocusActive==True:
            self.supremeMasterworkFocus()
            #Need to code this so as to count only successes, and only tag groups of three at a time.
            #Consider that some dice attribute 2 successes and others only 1
            while self.total_no_DIT_succ() // 3 > 1:
                self.supremeMasterworkFocus()
                no_DIT_succ=self.total_no_DIT_succ() // 3

                def check_successes_needed(successes, no_DIT_succ):
                    change_count = 0
                    changable=[]
                    for counter,dice in enumerate(successes):
                        if dice[0]>0 and self.dice_pool[counter].DITThree==False:
                            change_count+=dice[0]
                            changable.append(counter)
                        if change_count>=no_DIT_succ:
                            return changable

                if check_successes_needed(self.successes,no_DIT_succ)!=0:
                    for i in check_successes_needed(self.successes,no_DIT_succ):
                        self.dice_pool[i].DITThree=True

                #roll for every 3 successes (that haven't been rolled yet)
                self.roll(no_DIT_succ)
                print("Divine Inspired 3s!")

                #Alt implementation of HMU (aiding initial recursion)
                if self.HMUUsed==False:
                    self.roll(3)
                    self.HMUUsed=True

                #Add section for the last no_DIT_succ die, check successes, and roll extra HMU if 3+
                self.supremeMasterworkFocus()

                #One implementation of Holistic Miracle Understanding (crazy recursion)
                # if sum([item[0] for item in self.successes[-no_DIT_succ:]])>3:
                #     self.roll(3)
                #     print("Holistic extra 3s")

                print("Internal check %d" % self.total_succ())


            #Need to make sure the +3 from HMU is additional to the x//3 dice. not 3*(x//3)

            # #BAD IMPLEMENTATION - NEEDS DETECTING OF CURRENT NON DIT SUCCESSES
            # #Implementation of Holistic Miracle Understanding
            # if sum([dice_pool.DITThree for dice_pool in self.dice_pool])//3 >= 1:
            #     self.roll(3*sum([dice_pool.DITThree for dice_pool in self.dice_pool])//3)


        #This is for no Supreme masterwork focus (needs fixing)
        # else:
        #     self.success()
        #     no_DIT_succ=self.total_no_DIT_succ() // 3
        #     for roll in self.dice_pool:
        #         roll.DITThree = True
        #     self.roll(no_DIT_succ)
        #
        #     # Implementation of Holistic Miracle Understanding
        #     if sum([dice_pool.DITThree for dice_pool in self.dice_pool]) // 3 >= 1:
        #         self.roll(3 * sum([dice_pool.DITThree for dice_pool in self.dice_pool]) // 3)


class diceresult:
    def __init__(self,die):
        self.result=die
        self.tenreroll=False
        self.sixreroll=False
        self.FmoDThree=False
        self.DITThree=False
        self.success=self.success_check(self.result)

    def success_check(self,result):
        #Checks if result is a success and assigns a boolean
        success = result>=7
        return success

def Extract(lst,element):
    return [item[element] for item in lst]

#Return list of dice results from list of objects
#[dice_pool.result for dice_pool in fang.dice_pool]





Results=[]
for x in range(1,10000):
    fang = crafter(5, 5, essence=3, int=4, stunt=0, supremeMasterworkFocusActive=True, SMFAdvanced=True)
    # fang=crafter(1,1,essence=1,int=1,stunt=0,supremeMasterworkFocusActive=True,SMFAdvanced=True)
    # fang=crafter(2,2,essence=2,int=2,stunt=0,supremeMasterworkFocusActive=True,SMFAdvanced=True)

    fang.scenario()
    prev_res = -1
    while prev_res!=fang.total_succ():
    # while True:
        prev_res = fang.total_succ()
        fang.scenario_recur()
        print(fang.total_succ())
    Results.append(prev_res)

print(Results)
from seaborn import distplot
import matplotlib
distplot(Results)
matplotlib.pyplot.show()
# print(fang.total_succ())

# print(fang.dice_pool)
#
#
#
# fang.success()



# fang.dice_pool=[diceresult(1),diceresult(1),diceresult(1),diceresult(1),diceresult(9),diceresult(9),diceresult(9)]
# fang.firstMovementoftheDemiurge(True)
# [dice_pool.result for dice_pool in fang.dice_pool]
# [dice_pool.FmoDThree for dice_pool in fang.dice_pool]