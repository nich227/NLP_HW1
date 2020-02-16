import sys
import time
'''
Name: Kevin Chen
NetID: nkc160130
CS 6320
Due: 2/17/2020
Dr. Moldovan
'''


class Bigram:
    def __init__(self):
        self.bigramPairs = []
        self.words = []

    def __init__(self, bp, wds):
        self.bigramPairs = bp
        self.words = wds

# Takes in an input file and extracts the bigrams from it


def bigramParser(file):

    # Read in all words that are in the file
    words = []
    try:
        with open(file, 'r') as input:
            for ln in input:
                for wd in ln.split():
                    if wd == '.' or wd == '?' or wd == '!':
                        words.append('</s>')
                        words.append('<s>')
                    if wd.isalpha() or wd.isnumeric():
                        words.append(wd.lower())
            words.insert(0, '<s>')
    except FileNotFoundError:
        print("ERROR:", file, "not found!")
        exit(1)

    # Convert words to bigram pairs
    bigramPairs = []
    nextWord = 1
    for word in words:
        if nextWord < len(words):
            # Omitting useless bigram pair (</s>,<s>)
            if word != '</s>' and nextWord != '<s>':
                bigramPairs.append((word, words[nextWord]))
        nextWord += 1

    return Bigram(bigramPairs, words)

# Takes in an array of bigram pairs and calculates the probability for all bigrams to occur


def calcProbBigram(bigrams, smoothing):

    # Calculate number of times every word appears in the corpus (count(w2))
    for thisWord in bigrams.words:
        # Already checked word
        if thisWord in wordCounts:
            continue
        thisWordCount = 0
        for word in bigrams.words:
            if word == thisWord:
                thisWordCount += 1
        if smoothing == 1:
            thisWordCount += len(bigrams.words)
        wordCounts.update({thisWord: thisWordCount})

    # Calculate number of times every bigram appears in the corpus(count(w2 ^ w1))
    bigramCounts = {}
    for bigram in bigrams.bigramPairs:
        if smoothing == 0:
            bigramCounts.update({bigram: bigrams.bigramPairs.count(bigram)})
        if smoothing == 1:
            bigramCounts.update({bigram: bigrams.bigramPairs.count(bigram)+1})

    # Calculate the probability that a bigram appears in the corpus
    bigramProbs = {}
    for bigram in bigrams.bigramPairs:
        bigramProbs.update(
            {bigram: bigramCounts.get(bigram)/wordCounts.get(bigram[0])})

    return bigramProbs

# Calculates the probability of each sentence in test data
# given probabilities of bigrams in training data


def calcSentProb(bpsProbs, bpsTest, smoothing):
    sentenceProbs = {}
    sentence = []
    sentenceProb = 1
    testVocab = []

    # Get vocabulary of test data
    for word in bpsTest.words:
        if word in testVocab:
            continue
        testVocab.append(word)

    # Tables
    countsTable = {}
    probsTable = {}

    # Get sentences in corpus
    for bpTest in bpsTest.bigramPairs:
        # End of sentence
        if bpTest[1] == '</s>':

            # Run through one last time
            # Bigram exists in training data
            if bpTest in bpsProbs:
                sentenceProb *= bpsProbs.get(bpTest)
                countsTable.update(
                    {bpTest: int(bpsProbs.get(bpTest)*wordCounts.get(bpTest[0]))})
                probsTable.update({bpTest: bpsProbs.get(bpTest)})

            # Bigram doesn't exist in training data
            else:
                if(smoothing == 0):
                    sentenceProb *= 0.0
                    countsTable.update({bpTest: 0})
                    probsTable.update({bpTest: 0.0})
                if(smoothing == 1):
                    if bpTest[0] in wordCounts:
                        sentenceProb *= (1.0/wordCounts.get(bpTest[0]))
                        countsTable.update({bpTest: 1})
                        probsTable.update(
                            {bpTest: (1.0/wordCounts.get(bpTest[0]))})
                    else:
                        sentenceProb *= 0.0
                        countsTable.update({bpTest: 0})
                        probsTable.update({bpTest: 0})
            
            # Update sentence probabilities
            sentenceProbs.update({" ".join(sentence): sentenceProb})

            # Print and reset all sentence values
            print("Sentence:", " ".join(sentence))
            print("Counts:")
            for bigram in countsTable:
                print(bigram, ": ", countsTable[bigram], sep="")
            print("Probabilities:")
            for bigram in probsTable:
                print(bigram, ": ", probsTable[bigram], sep="")
            countsTable = {}
            probsTable = {}
            print("Overall sentence probability: ",
                  sentenceProb, "\n\n", sep='')

            sentence = []
            sentenceProb = 1

            continue

        # Bigram exists in training data
        if bpTest in bpsProbs:
            sentenceProb *= bpsProbs.get(bpTest)
            countsTable.update(
                {bpTest: int(bpsProbs.get(bpTest)*wordCounts.get(bpTest[0]))})
            probsTable.update({bpTest: bpsProbs.get(bpTest)})

        # Bigram doesn't exist in training data
        else:
            if(smoothing == 0):
                sentenceProb *= 0.0
                countsTable.update({bpTest: 0})
                probsTable.update({bpTest: 0.0})
            if(smoothing == 1):
                if bpTest[0] in wordCounts:
                    sentenceProb *= (1.0/wordCounts.get(bpTest[0]))
                    countsTable.update({bpTest: 1})
                    probsTable.update(
                        {bpTest: (1.0/wordCounts.get(bpTest[0]))})
                else:
                    sentenceProb *= 0.0
                    countsTable.update({bpTest: 0})
                    probsTable.update({bpTest: 0})

        sentence.append(bpTest[1])


# Driver that runs the program
start_time = time.time()

# Not running on Python 3.x
if sys.version_info < (3, 0):
    print("ERROR: This program requires Python 3.x or higher.")
    exit(1)

# Word counts for all words
wordCounts = {}

if len(sys.argv)-1 == 3:
    bigramTrain = bigramParser(sys.argv[1])
    probTrain = calcProbBigram(bigramTrain, int(sys.argv[3]))
    bigramTest = bigramParser(sys.argv[2])
    calcSentProb(probTrain, bigramTest, int(sys.argv[3]))
    print("-----\n", "HW1 took ", round(time.time() -
                                        start_time, 4), " seconds to complete.", sep="")

# Invalid number of arguments
else:
    print("ERROR: Invalid number of arguments!")
    print("Usage: hw1.py <training-set> <test-set> b")
    exit(1)
