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