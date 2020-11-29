import numpy as np

# CrafitngTry2.py
# Matt R
#### Trying to simplify the code problem down to just a linear logic (maybe some recursion is thrown in)
def roll(ndice):
    ##### Function so I don't have to copy randint everytime. (still have to append to the pool though)
    return [die(i) for i in (np.random.randint(1,11,ndice))]


class die:
    ####Class for a die, so I keep all the information about the state of a die together
    def __init__(self,roll):
        #Die Result
        self.result = roll
        #Is a ten, that has added a dice to the pool
        self.tenreroll = False
        #Is a 6, that has added a dice to the pool
        self.sixreroll = False
        #Has been considered as part of a three of a kind for First Movement of the Demiurge
        self.FmoDThree = False
        #Its successes have been counted towards a 3 success to add an extra die from Divine Inspiration Technique
        self.DITThree = False

    #How many successes does this die contribute - as property, updates with the any changes to the class instance
    #Eg, if FMoD changes it to a 10, it updates correctly.
    @property
    def die_success(self):
        # Dictionary of success responses (using SMF2)
        success_dict = {1: 0,
                        2: 0,
                        3: 0,
                        4: 0,
                        5: 0,
                        6: 0,
                        7: 1,
                        8: 2,
                        9: 2,
                        10: 2}
        return success_dict[self.result]

# def main():

# Dice to be rolled
n_dice = 10
experiential_dice = 10

# Initial dice pool
dice_results = roll(n_dice)

# Experiential Conjuring of the true void extra rolls
##Join lists
dice_results= dice_results + roll(experiential_dice)

# Now we enter Recursion Zone
#First are the simple ones - reroll 10s and 6s

# rerolltens(dice_results)


# if __name__ == "__main__":
#     main()

[res.result for res in dice_results]