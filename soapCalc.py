#!/usr/bin/python

# File name: soapCalc.py
# Author: Joseph Courtney
# Date: 3/4/2018
# This a python program that calculates the necessary amounts of liquids and
# lye(sodium hydroxide) in grams for a specific combination of fatty oils. It
# then outputs the full recipe. To run this program simply type python2.7
# josephcourtney_soapCalc.py. The program will then ask the user for the total
# number of oils, the total weight of oils and the necessary superfatting
# ratio. It then asks the user for the name of the oils they would like to use
# and their respective ratios. The program calculates the necessary variables
# and outputs the complete soap recipe for the user. It then gives the option
# to resize the batch by changing the total oil weight and gives the user the
# option to save the recipe to a text file. The program will output and error
# messages if the total percentage of oils is not 100 or if there is an unknown
# oil in the user input. DISCLAMER this only works on python2.7 due to its use
# of raw_input to read strings to run on python3 these must be changed to input

import sys
import os.path
import time

def main():
    """ Calculates, Outputs and Writes a soap recipe from prompted user input
    keywords:
        oils: list of known oils
        sap_ratios: list of SAP ratios corresponding to known oils list
        count: user input for number of recipe oils
        weight: user input for total weight of oils
        superfat: user input for superfat ratio in whole numbers
        oils_list: list of oils to be calculated from user input
        oil_weights: corresponding weights of user's oils
        sap_location: list of locations within sap_ratios
        ratio_list: list of oil weight ratios from user input
        lye_weight: calculated weight of sodium hydroxide
        liquid_weight: caclulated weight of liquids
        *** note to self redo with classes and dicts to consolidate ***
    """
    oils = ( "aloe", "apricotkernel", "avocado", "babussa", "beeswax", "canola", "castor", "cocoa", "coconut", "coffee", "corn", "cottonseed", "flaxseed", "grapeseed", "hazelnut", "hempseed", "jojoba", "lard", "mango", "mustard", "neem", "olive", "palm", "peanut", "pumpkinseed", "ricebran", "sesame", "shea", "soybean", "sunflower", "sweetalmond", "walnut")
    sap_ratios = ( 0.171, 0.135, 0.134, 0.179, 0.067, 0.123, 0.129, 0.138, 0.178, 0.134, 0.135, 0.137, 0.136, 0.135, 0.136, 0.138, 0.066, 0.138, 0.135, 0.123, 0.14, 0.135, 0.141, 0.135, 0.138, 0.135, 0.137, 0.128, 0.135, 0.136,  0.135, 0.138)

    count = 0
    weight = 0
    superfat = 0
    oils_list = []
    oil_weights = []
    sap_location = []
    ratio_list = []

    welcome(oils)
    count, weight, superfat = OWSValidation(count, weight, superfat)
    oils_list, sap_location = oilInput(count, oils)
    ratio_list = ratioInput(count, oils_list, ratio_list)
    oil_weights = weightCalc(ratio_list, weight)
    lye_weight = lyeCalc(oil_weights, sap_location, sap_ratios,superfat)
    liquid_weight = .33 * weight
    printRecipe(count, weight, oils_list, oil_weights,lye_weight, liquid_weight)
    reSize(count, weight, oils_list, oil_weights, superfat, sap_location, sap_ratios, ratio_list, lye_weight, liquid_weight)


def welcome(oils):
    """ Prints known oils list if prompted by the user
    args:
        oils: array of strings
    output:
        printed list of known oils
    """
    print ("\n***************** Welcome to Joe and Alanna's Soap Calculator *****************\n\n")
    answer = raw_input("Would you like to see the full list of oils recognized by this program(y/n)? ")

    if (answer is 'y'):
        print("*-----------------------------FULL OIL LIST-----------------------------------*\n")
        size = len(oils)
        x = 0
        while (x < size):
            print(oils[x])
            x = x + 1


def OWSValidation(count, weight, superfat):
    """ Tests user input for validity with trap loops and error testing.
    args:
        count: integer
        weight: integer
        superfat: integer
    returns:
        count: integer
        weight: integer
        superfat: integer
    error tests:
        SyntaxError: for user input of None or NULL or \n
        NameError: for user input of wrong type
    """
    while True:
        try:
            count = input("How many oils would you like to calculate(1-10): ")
        except (SyntaxError, NameError):
            continue
        else:
            count = int(count)
            if (count <= 0 or count > 10):
                continue
            else:
                break

    while True:
        try:
            weight = input("What is the total weight in grams of oils you would like to calculate: ")
        except (SyntaxError, NameError):
            continue
        else:
            weight = float(weight)
            if (weight <= 0):
                continue
            else:
                break

    while True:
        try:
            superfat = input("Enter a superfatting ratio (greater than 0): ")
        except (SyntaxError, NameError):
            continue
        else:
            superfat = float(superfat)
            if (superfat <= 0 or superfat > 100):
                continue
            else:
                break

    return count, weight, superfat


def oilInput(count, oils):
    """ Tests user input of specific oils for validity with trap loop.
    args:
        count: integer
        oils: array of strings
    returns:
        oils_list: array of strings; validated oils from user input
        sap_location: array of integers; element locals from valid oils
            in known oils list
    """
    index = 1
    oils_list = []
    sap_location = []

    while (index <= count):
        temp = raw_input("Enter oil number {0}: ".format(index))
        if temp in oils:
            oils_list.append(temp)
            sap_location.append(oils.index(temp))
            index = index + 1
        else:
            print("*** {0} oil not recognized ***\n".format(temp))

    return oils_list, sap_location


def ratioInput(count, oils_list, ratio_list):
    """ Tests user input of ratios of chosen recipe oils for validity
    args:
        count: integer
        oils_list: array of strings
        ratio_list: array of integers
    returns:
        ratio_list: array of integers; valid ratios corresponding to recipe oils
    """
    index = 0
    ratio_total = 0

    while (ratio_total != 100):     # trap loop to validate for 100%
        while (index < count):
            while True:
                try:
                    weight = input("Enter {0} oil's ratio in whole numbers({1} out of 100): ".format(oils_list[index], ratio_total))
                    weight = int(weight)
                except (SyntaxError, NameError):
                    continue
                else:
                    if (weight <= 0 or weight > 100):
                        print("*** Invalid Weight ***")
                        continue
                    else:
                        ratio_list.append(weight)
                        ratio_total = ratio_total + weight
                        index = index + 1
                        break
        if (ratio_total != 100):
            print ("*** The provided ratios equal {0} not 100 ***\n".format(ratio_total))
            ratio_total = 0      # resets accumulators, index and list of ratios
            index = 0
            ratio_list = []

    return ratio_list


def weightCalc(ratio_list, weight):
    """ Calculates weights of oils from given ratios and total oil weight
    args:
        ratio_list: array of integers
        weight: integer
    returns:
        oil_weights: array of floats; weights corresponding to recipe oils
    """
    oil_weights = []
    temp_weight = 0

    for ratio in ratio_list:
        ratio = float(ratio)
        temp_weight = (ratio / 100) * weight
        oil_weights.append(temp_weight)

    return oil_weights


def lyeCalc(weights, locations, sap_ratios, superfat):
    """ Calculates lye weight using the given ratios and corresponding locations in the SAP ratio list, taking into account the superfatting ratio
    args:
        oil_weights: array of floats
        locations: array of integers
        sap_ratios: array of integers
        superfat: integer
    returns:
        lye_weight: float; calculated weight of sodium hydroxide
    """
    lye_weight = 0
    index = 0

    for location in locations:
        temp_lye = sap_ratios[location] * weights[index]
        lye_weight = lye_weight + temp_lye
        index = index + 1
    lye_weight = lye_weight - ((superfat/100) * lye_weight)

    return lye_weight


def printRecipe(count, weight, oils, weights, lye, liquid):
    """ Outputs formatted recipe to command line terminal
    args:
        count: integer
        weight: integer
        oils: array of strings
        weights: array of floats
        lye: float
        liquid: float
    output:
        prints formatted recipe
    """
    index = 0
    print("\n")
    while (index < count):
        print ("{0} oil: {1} grams".format(oils[index], weights[index]))
        index = index + 1
    print("Lye(sodium hydroxide): {0} grams".format(lye))
    print("liquids: {0} grams".format(liquid))
    weight = weight + lye + liquid
    print("Total Batch Yield Weight: {0} grams".format(weight))


def reSize(count, weight, oils, weights, superfat, locations, sap_ratios, ratio_list, lye_weight, liquid):
    """ Recalculates recipe according to a new total oils weight, calls printRecipe to reprint the new recipe, and saveRecipe to save to .txt file
    args:
        count: integer
        weight: integer
        oils: array of strings
        weights: array of floats
        superfat: integer
        locations: array of integers
        sap_ratios: array of floats
        ratio_list: array of integers
        lye_weight: float
        liquid: float
    returns:
        printRecipe(): prints newly calculated recipe
        saveRecipe(): saves recipe to text file
    """
    answer = raw_input("Would you like to resize this recipe(y/n)? ")
    if (answer is 'y'):
        weight = 0
        weights = []
        lye_weight = 0

        while (weight <= 0):
            weight = input("What is the total weight in grams of oils you would like to calculate: ")

        weights = weightCalc(ratio_list, weight)
        lye_weight = lyeCalc(weights, locations, sap_ratios, superfat)
        liquid = .33 * weight
        printRecipe(count, weight, oils, weights, lye_weight, liquid)
        saveRecipe(count, weight, oils, weights, lye_weight, liquid)
    else:
        saveRecipe(count, weight, oils, weights, lye_weight, liquid)


def saveRecipe(count, weight, oils, weights, lye, liquid):
    """ Writes recipe to a text file with a title and a timestamp
    args:
        count: integer
        weight: integer
        oils: array of strings
        weights: array of floats
        lye: float
        liquid: float
    output:
        if soap_recipes.txt does not exist: creates new .txt file, writes recipe
        if soap_recipes.txt exists: appends .txt file with new recipe
        prints closing message
        exit()
    """
    answer = raw_input("Would you like to save this recipe to a text file (y/n)? ")
    if (answer is 'y'):
        if os.path.exists('soap_recipes.txt'):
            recipe = open("soap_recipes.txt", "a")
        else:
            recipe = open("soap_recipes.txt", "w")

        localtime = time.asctime( time.localtime(time.time())) # from time
        recipe.write("\n** {0} **\n".format(localtime))     # recipe timestamp

        title = raw_input("\nWhat would you like to call your soap recipe? ")
        recipe.write("---- {0} ----\n".format(title))       # recipe title

        index = 0
        while (index < count):
            recipe.write("{0} oil: {1} grams\n".format(oils[index], weights[index]))
            index = index + 1

        recipe.write("Lye(sodium hydroxide): {0} grams\n".format(lye))
        recipe.write("liquids: {0} grams\n".format(liquid))
        weight = weight + lye +liquid
        recipe.write("Total Batch Yield Weight: {0} grams\n".format(weight))
        recipe.close()

        print("\n************* Thank You For Using Joe and Alanna's Soap Calculator *************\n")
        sys.exit()
    else:
        print("\n************* Thank You For Using Joe and Alanna's Soap Calculator *************\n")
        sys.exit()


if __name__ == '__main__':
    main()
