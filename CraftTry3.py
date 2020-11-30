import pandas as pd
import numpy as np
from itertools import combinations
from math import inf
from collections import Counter

def roll(ndice):
    ##### Function so I don't have to copy randint everytime. (still have to append to the pool though)
    pool = pd.DataFrame({'result':np.random.randint(1,11,ndice)})
    pool['tenreroll'] = False
    pool['sixreroll'] = False
    pool['FmoDThree'] = False
    pool['DITThree'] = False
    return pool

def rerolltens(dice_res):
    #Index tens to find "good tens" tens that haven't been rerolled yet
    good_tens=(dice_res['result'] == 10) & (dice_res['tenreroll'] == False)
    while sum(good_tens)!=0:
        #based on the good_tens index, assign that they are about to be rerolled (and are 'bad tens')
        dice_res.loc[good_tens,'tenreroll']=True
        #roll the number of goodten dice and return the final dataframe - you need to save this output, as the tenreroll assignment happens inplace for some reason
        dice_res = dice_res.append(roll(sum(good_tens)), ignore_index=True, sort=True)
        # Index tens to find "good tens" tens that haven't been rerolled yet
        good_tens = (dice_res['result'] == 10) & (dice_res['tenreroll'] == False)
    return dice_res

def rerollsixes(dice_res):
    #Index sixes to find "good sixes" sixes that haven't been rerolled yet
    good_sixes=(dice_res['result'] == 6) & (dice_res['sixreroll'] == False)
    while sum(good_sixes)!=0:
        #based on the good_sixes index, assign that they are about to be rerolled (and are 'bad sixes')
        dice_res.loc[good_sixes,'sixreroll']=True
        #roll the number of goodten dice and return the final dataframe - you need to save this output, as the tenreroll assignment happens inplace for some reason
        dice_res = dice_res.append(roll(sum(good_sixes)), ignore_index=True, sort=True)
        # Index sixes to find "good sixes" sixes that haven't been rerolled yet
        good_sixes = (dice_res['result'] == 6) & (dice_res['sixreroll'] == False)
    return dice_res

def dicererolls(dice_res,success_dict):
    #Complete all rerolls in a recusive mannerr
    len_beginning = len(dice_res)
    len_end = len(dice_res)+1
    #Check that length of dataframe hasn't changed
    while len_beginning != len_end:
        len_beginning=len(dice_res)
        dice_res=rerollsixes(dice_res)
        dice_res=rerolltens(dice_res)
        #temporary add firstmovement of demiurge to loop
        dice_res=firstMovementoftheDemiurge(dice_res)
        dice_res=divineInspirationTechnique(dice_res,success_dict,HMU=False)
        print(sum(dice_res['result'].map(success_dict)))
        len_end=len(dice_res)
    return dice_res

def firstMovementoftheDemiurge(dice_res):
    # First Movement of the Demiurge
    # For every three of a kind successes (ex: three sevens, three eights, etc.), the player may choose one non-success die
    # and convert it to a 10, adding two successes to the result. If Flawless Handiwork Method is used, 10s created in this
    # fashion are also rerolled until 10s fail to appear.

    #Create sublist of undemiurged
    demi_false=dice_res['FmoDThree']==False

    #Return unique values of in dice rolls
    counts = dice_res[demi_false]['result'].value_counts()

    #Ensure you only use successful counts
    succ_counts=counts[counts.keys()>6]

    #Check which dice results have an output divisible by 3
    conversion_nums=succ_counts.floordiv(3)

    #Change the FmoDThree state on 3 * counversion_nums of each number to True
    used_dice=conversion_nums*3


    for index, value in used_dice.items():
        # dice_res[dice_res['result']==index][:value]['FmoDThree']=True
        # dice_res.loc[dice_res[dice_res['result'] == index].iloc[:value], 'FmoDThree'] = True
        dice_res.loc[dice_res[dice_res['result'] == index].index[:value], 'FmoDThree']=True

    #convert the first non successes (below 7s) to 10s,
    # I really should clear their sixreroll state, but it shouldn't have any effect later
    # dice_res[dice_res<7][:sum(conversion_nums)]['result']=10
    dice_res.loc[dice_res[dice_res['result'] < 7].index[:sum(conversion_nums)], 'result']=10

    return dice_res


def divineInspirationTechnique(dice_res,success_dict,HMU=False):
    # def close_finder(numbers,target):
    #     # numbers = [1, 2, 3, 4]
    #     # target = 9
    #     best_combination = ((None,))
    #     best_result = inf
    #     best_sum = 0
    #
    #     # generate all combinations of the numbers
    #     # including combinations with different lengths
    #     for L in range(0, len(numbers) + 1):
    #         for combination in combinations(numbers, L):
    #             sum = 0
    #             for number in combination:
    #                 sum += number
    #             result = target - sum
    #             if abs(result) < abs(best_result):
    #                 best_result = result
    #                 best_combination = combination
    #                 best_sum = sum
    #                 # print("\nnew best\n{}\nsum:{} off by:{}".format(best_combination, best_sum, best_result))
    #
    #     return best_combination

    #need to implement in a less computationally bad way
    def close_finder(numbers,target):
        numbers=np.array(numbers)
        current_sum=0
        used = []
        for idx,i in enumerate(numbers):
            if i == 2:
                used.append(i)
            if any(numbers==2)==False:
                used.append(i)
            # print("appended")
            if sum(used)==target:
                print("Maybe all twos")
                return used
            if sum(used)>target:
                if any(numbers==1):
                    used = used[:1]
                    used.append(numbers[numbers==1][0])
                    print("add a one")
                    return used
                else:
                    print(str(-1))
                    return used[:-1]
            if used.count(2)==len(numbers[numbers==2]):
                while sum(used)!=target:
                    used.append(1)
                return used
            if idx==len(numbers)-1:
                print("why?")


    dice_res['successes'] = dice_res['result'].map(success_dict)
    total_DIT_successes = sum(dice_res.loc[dice_res['DITThree'] == False, 'successes'])

    successes_to_tag=(total_DIT_successes//3)*3

    #Check for valid combination of successes to make required sum (>0 handily discludes nans from this)
    success_combos_pool=close_finder(dice_res[(dice_res['successes']>0) & (dice_res['DITThree']==False)]['successes'],successes_to_tag)

    # #For some reason success_combos_pool can close empty need to fix
    # if success_combos_pool==None:
    #     exit()

    #Convert to counter to make it easier
    success_combos=Counter(success_combos_pool)
    #dirty hard coding
    dice_res.loc[dice_res[(dice_res['successes'] == 1) & (dice_res['DITThree']==False)].index[:success_combos[1]], 'DITThree'] = True
    dice_res.loc[dice_res[(dice_res['successes'] == 2) & (dice_res['DITThree']==False)].index[:success_combos[2]], 'DITThree'] = True


    if HMU==True:
        dice_res = dice_res.append(roll((total_DIT_successes // 3)+3), ignore_index=True, sort=True)

    else:
        dice_res = dice_res.append(roll(total_DIT_successes//3), ignore_index=True, sort=True)



    # #Partially working generator function to find the next sublist that created the desired successes to change
    # def subset_sum(numbers, target, partial=[], partial_sum=0):
    #     if partial_sum == target:
    #         yield partial
    #     if partial_sum >= target:
    #         return
    #     for i, n in enumerate(numbers):
    #         remaining = numbers[i + 1:]
    #         yield from subset_sum(remaining, target, partial + [n], partial_sum + n)


    return dice_res.drop('successes',axis=1)



# Dice to be rolled
n_dice = 10
experiential_dice = 10

# Initial dice pool
dice_results = roll(n_dice)

# Experiential Conjuring of the true void extra rolls
##Append rows to pool list
dice_results= dice_results.append(roll(experiential_dice), ignore_index=True,sort=True)


# Now we enter Recursion Zone

#First are the simple ones - reroll 10s and 6s (Flawless Handwork Method 2)
# #Reroll 10s
# dice_results=rerolltens(dice_results)
# #Reroll 6s
# dice_results=rerollsixes(dice_results)

# Reroll 10s and 6s
# dice_results = dicererolls(dice_results,)



#Supreme Masterwork Focus (double 8s) is implemented through a modified success dictionary (change to standard or double 7s for those)
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

dice_results = dicererolls(dice_results,success_dict)

total_successes = sum(dice_results['result'].map(success_dict))
print("Total number of successes is: %i" % total_successes)

#First Movement of the Demiurge
# For every three of a kind successes (ex: three sevens, three eights, etc.), the player may choose one non-success die
# and convert it to a 10, adding two successes to the result. If Flawless Handiwork Method is used, 10s created in this
# fashion are also rerolled until 10s fail to appear.

#Temporarily aded to dicererolls
# dice_results=firstMovementoftheDemiurge(dice_results)




# if __name__ == "__main__":
#     main()





####CODE DUMP
#Returns slice of full pool of just result and tenroll
    # dice_results[dice_results.columns[dice_results.columns.isin(['result', 'tenreroll'])]]