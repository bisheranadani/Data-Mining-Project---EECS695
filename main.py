import numpy as np
import pandas as pd
from itertools import islice
import sys
import os

### UNCOMMENT THE NEXT LINE FOR HIGH MAXSTAR TO AVOID STACK OVERFLOW  ###
# sys.setrecursionlimit(20000)


def main():
    # print("start")
    print("Welcome to AQ algorithm!")
    txtfilename = input("Input text filename: ")
    while not os.path.isfile(txtfilename):
        print(os.path.isfile(txtfilename))
        print("Invalid filename, enter again: ")
        txtfilename = input("Input text filename: ")

    MAXSTAR = 5
    while True:
        tempMAXSTAR = input("Input MAXSTAR: ")
        try:
            MAXSTAR = int(float(tempMAXSTAR))
        except ValueError:
            pass
        if isinstance(MAXSTAR, int) and MAXSTAR > 0:
            break
        print("Input valid MAXSTAR")

    try:
        data = pd.read_csv(txtfilename, delim_whitespace=True, header=None, skiprows=2, dtype='str')
        column_names = ''
        with open(txtfilename) as file:
            for line in islice(file, 1, 2):
                column_names = line
    except IOError:
        print("Could not read file, aborting...")
        return

    column_names = column_names.split()[1:-1]
    data.columns = column_names
    attitude_name = column_names[-1]
    list_of_attitudes = set(data[attitude_name].unique())
    # print(list_of_attitudes)
    list_of_attributes = set(column_names[:-1])
    # print(data)
    attributedict = {}
    for attr in list_of_attributes:
        attributedict[attr] = set(data[attr].unique())
    # print(attributedict)
    column_names = set(column_names)

    # mydict_attitude = set(data.loc[(data['attitude'] == 'negative')].index.values)
    fullindex = set(data.index.values.tolist())

    # print(checkconsistent(data, list_of_attributes, attitude_name))

    if not checkconsistent(data, list_of_attributes, attitude_name):
        with open("my-data.with.negation.rul", 'w') as outputfile:
            outputfile.write("! The input data set is inconsistent !")
        with open("my-data.without.negation.rul", 'w') as outputfile:
            outputfile.write("! The input data set is inconsistent !")
        print("Data set inconsistent, aborting...")
        return

    print("start")
    finalruleset = {}
    for attitude in list_of_attitudes:
        mydict_attitude = set(data.loc[(data[attitude_name] == attitude)].index.values)
        finalruleset[attitude] = AQalgo(data, fullindex, mydict_attitude, list_of_attributes, MAXSTAR)
    print(finalruleset)
    printfileWithNegation(finalruleset)
    printfileWithoutNegation(finalruleset, attributedict)
    print("end")


def strgenerator(star):
    finalstr = """"""
    strdatabgn = "(data['"
    strdatabgncls = "'] != '"
    strvalcls = "')"
    strand = " & "
    stror = " | "
    count2 = 0

    for dict in star:
        if count2 > 0:
            finalstr = finalstr + stror
        count2 = count2 + 1
        finalstr = finalstr+"("
        count = 0
        for key in dict:
            if count > 0:
                finalstr = finalstr + strand
            keystr = key
            if("!!!" == key[-3:]):
                keystr = key[:-3]
            finalstr = finalstr + strdatabgn + keystr + strdatabgncls + dict[key] + strvalcls
            count = count + 1
        finalstr = finalstr + ")"

    return finalstr


def starconjunction(partialstar1, partialstar2, MAXSTAR):
    # MAXSTAR = 5
    returnarray = []
    if len(partialstar1) == 0:
        if len(partialstar2) == 0:
            return []
        return partialstar2
    elif len(partialstar2) == 0:
        return partialstar1

    for dict in partialstar1:
        for dictn in partialstar2:
            for key in dictn:
                tempdict = dict.copy()
                keystring = key
                if (key in tempdict) and (tempdict[key] != dictn[key]):
                    keystring = keystring+"!!!"
                tempdict[keystring] = dictn[key]
                returnarray.append(tempdict)
                if len(returnarray) > MAXSTAR:
                    return returnarray



    return returnarray



def AQalgo(data, fullindex, attitudeset, list_of_attributes, MAXSTAR):
    iterset = fullindex.difference(attitudeset)
    # print (iterset)
    cover = set({})
    temp_cover = {}
    final_star = []
    temp_final_star = []
    seed_first = True
    for seed in attitudeset:
        # print("seed: ", seed)
        if seed_first or seed not in cover:
            flag_index_first = True
            temp_cover = set({})
            temp_final_star = []
            for index in iterset:
                # print("index: ", index)
                if flag_index_first or (seed_first and index in cover) or ((not seed_first) and index in temp_cover):
                    flag_index_first = False
                    partialstar_temp = []
                    for attr in list_of_attributes:
                        if data.at[seed, attr] != data.at[index, attr]:
                            tempdict = {attr: data.at[index, attr]}
                            partialstar_temp.append(tempdict)
                    # print("partialstar_temp for index", index, partialstar_temp)
                    if seed_first:
                        final_star = starconjunction(final_star, partialstar_temp, MAXSTAR)
                        reduceAQruleset(final_star)
                        stringcondition = strgenerator(final_star)
                        cover = set(data.loc[eval(stringcondition)].index.values)
                        # print("final_star first seed:", final_star)
                        # print("cover first seed: ", cover)
                    else:
                        temp_final_star = starconjunction(temp_final_star, partialstar_temp, MAXSTAR)
                        reduceAQruleset(temp_final_star)
                        stringcondition = strgenerator(temp_final_star)
                        temp_cover = set(data.loc[eval(stringcondition)].index.values)
                        # print("final_star NOT first seed: ", temp_final_star)
                        # print("cover NOT first seed: ", temp_cover)
            cover = cover.union(temp_cover)
            for dict in temp_final_star:
                final_star.append(dict)
            reduceAQruleset(final_star)
            # print(final_star)
            seed_first = False
            # print("last cover: ", cover)
            # print("last final_star", final_star)

    # print("CLOSING FINAL STAR:", final_star)
    return final_star


def startotextrule(star, attitude, withoutnegation, attrdic=[]):
    stringarray = []
    strnot = " not "
    for dict in star:
        count1 = 0
        tempstr = ""
        for key in dict:
            keystr = key
            if key[-3:] == '!!!':
                keystr = key[:-3]
            if count1 > 0:
                tempstr = tempstr + " & "
            attvalue = dict[key]
            if withoutnegation:
                strnot = " "
                attvalue = ""
                count2 = 0
                for val in attrdic[keystr]:
                    if val != dict[key]:
                        if count2 > 0:
                            attvalue = attvalue + " or "
                        attvalue = attvalue + val
                        count2 += 1
            tempstr = tempstr + "(" + keystr + ","+strnot+ attvalue + ")"
            count1 += 1
        tempstr = tempstr + " -> (attitude, " + attitude +")"
        stringarray.append(tempstr)
        # print(tempstr)
    return stringarray

def reduceAQruleset(ruleset):
    singleslist = []
    singlesindex = set({})
    incindex = set({})

    i = -1
    for dict in ruleset:
        i += 1
        if len(dict) == 1:
            singleslist.append(dict)
            singlesindex.add(i)

    if not(len(singlesindex) > 0):
        return
    # print(singlesindex)
    # print(singleslist)

    for somerule in singleslist:
        for key in somerule:
            for i in range(len(ruleset)):
                # if i not in singlesindex and key in ruleset[i]:
                #     keystr = key + '!!!'
                #     if somerule[key] == ruleset[i][key] or somerule[key] == ruleset[i][keystr]:
                #         incindex.add(i)
                if i not in singlesindex:
                    keystr = key + '!!!'
                    if key in ruleset[i] and ruleset[i][key] == somerule[key]:
                        incindex.add(i)
                    if keystr in ruleset[i] and ruleset[i][keystr] == somerule[key]:
                        incindex.add(i)

    # print(incindex)

    if len(incindex) > 0:
        indices = sorted(incindex, reverse=True)
        for i in indices:
            del ruleset[i]


    # print(ruleset)


def printfileWithNegation(ruleset):
    # outputfile = open("my-data.with.negation.rul", w)
    with open("my-data.with.negation.rul", 'w') as outputfile:
        for key in ruleset:
            rulesetarray = startotextrule(ruleset[key], key, False)
            for rule in rulesetarray:
                # print(rule)
                outputfile.write(rule)
                outputfile.write('\n')

    outputfile.close()

    return

def printfileWithoutNegation(ruleset, attrdict):
    # outputfile = open("my-data.with.negation.rul", w)
    with open("my-data.without.negation.rul", 'w') as outputfile:
        for key in ruleset:
            rulesetarray = startotextrule(ruleset[key], key, True, attrdict)
            for rule in rulesetarray:
                # print(rule)
                outputfile.write(rule)
                outputfile.write('\n')

    outputfile.close()

    return

def checkconsistent(data, attrlist, aname):
    # print(attrlist, aname)
    for i in range(len(data.index)):
        for j in range(i, len(data.index)):
            incons = False
            for attr in attrlist:
                if data.at[i, attr] != data.at[j, attr]:
                    incons = False
                    break
                incons = True
            if incons:
                if data.at[i, aname] != data.at[j, aname]:
                    print("i,j: " , i,j)
                    return False

    return True






main()
