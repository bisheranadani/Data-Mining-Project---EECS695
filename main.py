import numpy as np
import pandas as pd
from itertools import islice


def main():
    print('Hello World\n')
    data = pd.read_csv('test.txt', delim_whitespace=True, header=None, skiprows=2)
    print (data)

    column_names = ''
    with open('test.txt') as file:
        for line in islice(file, 1, 2):
            print(line)
            column_names = line

    print(column_names.split())
    column_names = column_names.split()[1:-1]
    print(column_names)
    data.columns = column_names
    print(data)
# def read_word(fileobj):
#     for line in fileobj:
#         for token in line.split():
#             yield token
#
#
# def main():
#     print("Hello, World!")
#     filename = input("Please input the name of the file: ")
#     print(filename, ' is the name of the file')
#
#     with open(filename, 'r') as file:
#         words = read_word(file)
#         for i in range(50):
#             aword = next(words)
#             print(aword)
#
#     print('goodbye')
#

main()
