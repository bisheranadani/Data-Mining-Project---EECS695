def read_word(fileobj):
    for line in fileobj:
        for token in line.split():
            yield token
def main():
    print "Hello, World!"
    filename = raw_input("Please input the name of the file: ")
    print filename+' is the name of the file'

    with open(filename, 'r') as file:
        words = read_word(file)
        for i in range(50):
            aword = next(words)
            print aword


        # firstword = next(words)
        # secondword = next(words)
        #
        # print firstword, secondword
        # for word in words:
        #     print word




    print 'goodbye'
main()

