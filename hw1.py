import sys
'''
Name: Kevin Chen
NetID: nkc160130
CS 6320
Due: 2/17/2020
Dr. Moldovan
'''

# Takes in an input file and extracts the bigrams from it.


def bigramParser(file):
    words = []
    try:
        with open(file, 'r') as input:
            for ln in input:
                for wd in ln.split():
                    if wd.isalpha():
                        words.append(wd)    
    except FileNotFoundError:
        print("ERROR:", file, "not found!")
        exit(1)

    # Do something with words here

bigramParser(sys.argv[1])
