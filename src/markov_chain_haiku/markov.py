import math 
import random
from collections import defaultdict
from syllable_counter import count_syllables_word, count_syllables_text
import sys
import time


def getSuffix(prefix, dictionary, syllables = float('inf') , alike = False):
    suffixes = dictionary[prefix]
    if len(suffixes) == 0:
        return ""
    counts = {}
    biggestValue = 0
    biggestSuffix = ""
    for suffix in suffixes:
        if count_syllables_word(suffix) <= syllables:
            if suffix in counts:
                counts[suffix] += 1
            else:
                counts[suffix] = 1
            if counts[suffix] > biggestValue:
                biggestValue = counts[suffix]
                biggestSuffix = suffix
    return biggestSuffix

def getRandomWord(dictionary):
    words = list(dictionary.keys())
    index = random.randrange(0, len(words))
    return words[index]

def getFirstFittingSuffix(dictionary, key, syllables):
    suffixes = dictionary[key]
    for s in suffixes:
        if count_syllables_word(s) <= syllables:
            return s



    
def prepTraining(file):
    with open(file) as f:
        raw_haiku = f.read()
    corpus = raw_haiku.replace('\n','').split()
    
    return corpus

def map_word_to_word(corpus):
    limit = len(corpus) - 1
    dict1_to_1 = defaultdict(list)
    for index,word in enumerate(corpus):
        if index < limit:
            suffix = corpus[index + 1]
            dict1_to_1[word].append(suffix)
    return dict1_to_1

def map2_word_to_word(corpus):
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index,word in enumerate(corpus):
        if index < limit:
            partOfPrefix = corpus[index + 1]
            suffix = corpus[index + 2]
            dict2_to_1[word,partOfPrefix].append(suffix)
    return dict2_to_1

    
def writeHaiku(corpusM1,corpusM2):
    
    haiku = ""
    targetSyllables = 5
    first = ""
    while(first == "" or count_syllables_word(first) > targetSyllables):
        first = getRandomWord(corpusM1)
    haiku = first[0].upper() + first[1:]
    second = getSuffix(first, corpusM1,targetSyllables-count_syllables_word(first))
    if(second == ""):
        return "Your Haiku is too short \n" + "In its stead, you will get \n" + "this! a shameful attempt"
    haiku += " " + second

    line = haiku
    prefix = (first,second)
    i = 0
    while(i < 3):  # Veldig mange problemer her i denne løkken, må prøve å gjøre alt på nytt. 
        if(i == 1):
            targetSyllables = 7
        else: 
            targetSyllables = 5

        suffix = getSuffix(prefix, corpusM2, targetSyllables-count_syllables_text(line))
        if suffix == "":
            c = haiku[-1]
            while( c != ' '):
                haiku = haiku[:-1]
                line = line[:-1]
                c = haiku[-1]
            haiku = haiku[:-1]
            line = line[:-1]
            prefix = getRandomWord(corpusM2)
            while(count_syllables_text(prefix[0] + " " + prefix[1]) > targetSyllables - count_syllables_text(line)):
                prefix = getRandomWord(corpusM2)
            haiku += " (" + prefix[0] + " " + prefix[1] + ")"
            line += " (" + prefix[0] + " " + prefix[1] + ")"
        else:
            prefix = prefix[1],suffix
            haiku += " " + suffix
            line += " " + suffix
        if(count_syllables_text(line) == targetSyllables):
            haiku += "\n"
            line = ""
            i += 1
    return haiku

def main():
    corpus = prepTraining('src/markov_chain_haiku/resources/train.txt')
    corpusM1 = map_word_to_word(corpus)
    corpusM2 = map2_word_to_word(corpus)
    haiku = writeHaiku(corpusM1, corpusM2)
    print(haiku)


if __name__ == "__main__":
    main()
