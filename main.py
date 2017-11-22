import numpy as np
import pandas as pd
from itertools import islice


def setconjunction(temparr, temparr2):
    tempstar = []
    tempx = []
    if len(temparr) == 0:
        if len(temparr2) == 0:
            return []
        return temparr2
    elif len(temparr2) == 0:
        return temparr

    for xarray in temparr:
        for yarray in temparr2:
            for dict in yarray:
                tempx = xarray.copy()
                tempx.append(dict)
                tempstar.append(tempx)

    return tempstar

def strgenerator(star):
    finalstr = """"""
    strdatabgn = "(data['"
    strdatabgncls = "'] != '"
    strvalcls = "')"
    strand = " & "
    stror = " | "
    count2 = 0
    for array in star:
        count = 0
        if count2 > 0:
            finalstr = finalstr + stror
        count2 = count2 + 1
        finalstr = finalstr+"("
        for dict in array:
            for key in dict:
                if count > 0:
                    finalstr = finalstr + strand
                finalstr = finalstr + strdatabgn + key + strdatabgncls + dict[key] + strvalcls
                count = count + 1
        finalstr = finalstr+")"

    return finalstr


def main():
    data = pd.read_csv('testdata.txt', delim_whitespace=True, header=None, skiprows=2, dtype='str')
    print(data)

    column_names = ''
    with open('testdata.txt') as file:
        for line in islice(file, 1, 2):
            column_names = line

    column_names = column_names.split()[1:-1]
    print(column_names)
    data.columns = column_names
    attitude = column_names[-1]
    print(data[attitude].unique().tolist())
    list_of_attitudes = data[attitude].unique().tolist()
    list_of_attributes = column_names[:-1]
    print(list_of_attributes)
    mydict_attitude = {}
    mydict_attitude['positive'] = data.loc[(data['attitude'] == 'positive')].index.values.tolist()
    mydict_attitude['negative'] = data.loc[(data['attitude'] == 'negative')].index.values.tolist()



    star = []
    fullindex = data.index.values.tolist()


    # print(data.loc[eval(finalstr)].index.values.tolist())

    # seed = (mydict_attitude['positive'][0])
    # seedarray = [0, 1]
    # star = []
    # for x in fullindex:
    #     if x not in mydict_attitude['positive']:
    #         if x in seedarray:
    #             temparr = []
    #             for attr in list_of_attributes:
    #                 if data.at[seed, attr] != data.at[x, attr]:
    #                     temp = [{attr: data.at[x, attr]}]
    #                     temparr.append(temp)
    #             tempstar = []
    #             tempstar = setconjunction(star, temparr)
    #             star = tempstar
    #             finalstr = strgenerator(star)
    #             seedarray = data.loc[eval(finalstr)].index.values.tolist()
    #         else:
    #             print('-')

    # print(seedarray)
    # print(star)

    # seed = (mydict_attitude['negative'][0])
    seedarray = [1]
    finalstar = []
    for seed in mydict_attitude['negative']:
        star = []
        if (seed not in seedarray) or seed == mydict_attitude['negative'][0]:
            seedarray.append(0)
            print("seed", seed)
            print("seedarray", seedarray)
            if set(seedarray) == set(mydict_attitude['negative']):
                print("breaking")
                break
            for x in fullindex:
                if x not in mydict_attitude['negative'] or x in seedarray:
                    temparr = []
                    for attr in list_of_attributes:
                        print("x - attribute", x, attr)
                        if data.at[seed, attr] != data.at[x, attr]:
                            temp = [{attr: data.at[x, attr]}]
                            temparr.append(temp)
                            print("temparr", temparr)
                    tempstar = []
                    tempstar = setconjunction(star.copy(), temparr.copy())
                    for array in tempstar:
                        finalstar.append(array)
                    # star.append(tempstar)
                    finalstr = strgenerator(finalstar)
                    print("finalstr", finalstr)
                    seedarray = data.loc[eval(finalstr)].index.values.tolist()
                    break

    print(seedarray)
    print(star)

    coveredlist = []

    # temparr = []
    # for row in mydict_attitude['negative']:
    #     seed = row
    #     seedarray = [seed, 0]
    #     star = []
    #     for x in fullindex:
    #         if x not in mydict_attitude['negative']:
    #             if x in seedarray:
    #                 for attr in list_of_attributes:
    #                     if data.at[seed, attr] != data.at[x, attr]:
    #                         temp = [{attr: data.at[x, attr]}]
    #                         temparr.append(temp)
    #                 tempstar = []
    #                 tempstar = setconjunction(star, temparr)
    #                 star = tempstar
    #                 finalstr = strgenerator(star)
    #             else:
    #                 print('-')
    #         seedarray = data.loc[eval(finalstr)].index.values.tolist()

    # print(seedarray)
    # print(star)


    # finalstars = []
    # for attitude in mydict_attitude:
    #     attitude_rows = mydict_attitude[attitude]
    #     seedarray =[seed, 1]
    #     while (not set(seedarray).issubset(attitude_rows)) and len(seedarray) != len(attitude_rows):
    #         for row in attitude_rows:
    #             seed = row
    #             if row not in seedarray:
    #                 for x in fullindex:
    #                     if x not in mydict_attitude[attitude]:
    #                         if x in seedarray:
    #                             temparr = []
    #                             for attr in list_of_attributes:
    #                                 if data.at[seed, attr] != data.at[x, attr]:
    #                                     temp = [{attr: data.at[x, attr]}]
    #                                     temparr.append(temp)
    #                             tempstar = []
    #                             tempstar = setconjunction(star, temparr)
    #                             star = tempstar
    #                             finalstr = strgenerator(star)
    #                             seedarray = data.loc[eval(finalstr)].index.values.tolist()
    #                         else:
    #                             print('-')
    #




main()
