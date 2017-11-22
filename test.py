import numpy as np
import pandas as pd
from itertools import islice

def main():
    data = pd.read_csv('testdata.txt', delim_whitespace=True, header=None, skiprows=2, dtype='str')

    column_names = ''
    with open('testdata.txt') as file:
        for line in islice(file, 1, 2):
            column_names = line
    column_names = column_names.split()[1:-1]
    data.columns = column_names
    attitude_name = column_names[-1]
    list_of_attitudes = data[attitude_name].unique()
    list_of_attributes = set(column_names[:-1])
    print(data)

    # exdict = [{'size': 'large'}, {'ink-color': 'red'}]
    # exdict2 = [{'ink-color': 'blue'}]
    # print(starconjunction(exdict, exdict2))
    # print(strgenerator(starconjunction(exdict, exdict2)))

    # print(strgenerator(exdict))
    # print(starconjunction(exdict, exdict2))
    # print(strgenerator(starconjunction(exdict, exdict2)))

    mydict_attitude = set(data.loc[(data['attitude'] == 'negative')].index.values)
    fullindex = set(data.index.values.tolist())
    # print(mydict_attitude, list_of_attributes)
    # print(firstnumseed(mydict_attitude, fullindex), mydict_attitude)

    AQalgo(data, fullindex, mydict_attitude, list_of_attributes)

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


def starconjunction(partialstar1, partialstar2):
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


    return returnarray


# def firstnumseed(shortlist, longlist):
#     for x in longlist:
#         if x not in shortlist:
#             return x
#
#     return 0


def AQalgo(data, fullindex, attitudeset, list_of_attributes):
    iterset = fullindex.difference(attitudeset)
    print (iterset)
    cover = set({})
    temp_cover = {}
    final_star = []
    temp_final_star = []
    seed_first = True
    for seed in attitudeset:
        print("seed: ", seed)
        if seed_first or seed not in cover:
            flag_index_first = True
            temp_cover = set({})
            temp_final_star = []
            for index in iterset:
                print("index: ", index)
                if flag_index_first or (seed_first and index in cover) or ((not seed_first) and index in temp_cover):
                    flag_index_first = False
                    partialstar_temp = []
                    for attr in list_of_attributes:
                        if data.at[seed, attr] != data.at[index, attr]:
                            tempdict = {attr: data.at[index, attr]}
                            partialstar_temp.append(tempdict)
                    print("partialstar_temp for index", index, partialstar_temp)
                    if seed_first:
                        final_star = starconjunction(final_star, partialstar_temp)
                        stringcondition = strgenerator(final_star)
                        cover = set(data.loc[eval(stringcondition)].index.values)
                        print("final_star first seed:", final_star)
                        print("cover first seed: ", cover)
                    else:
                        temp_final_star = starconjunction(temp_final_star, partialstar_temp)
                        stringcondition = strgenerator(temp_final_star)
                        temp_cover = set(data.loc[eval(stringcondition)].index.values)
                        print("final_star NOT first seed: ", temp_final_star)
                        print("cover NOT first seed: ", temp_cover)
            cover = cover.union(temp_cover)
            for dict in temp_final_star:
                final_star.append(dict)
            seed_first = False
            print("last cover: ", cover)
            print("last final_star", final_star)

    print("CLOSING FINAL STAR:", final_star)
    return final_star


def startotextrule(star):
    for dict in star:
        finalstr = ""
        for key in dict:
            tempstr = "("+key+","+" not "+"dict[key]"



main()
