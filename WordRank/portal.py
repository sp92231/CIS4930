"""
Assignment 2: WordRank
Author: Shanie Portal
Semester: Spring 2024
Description: This file implements a simple tokenizaiton scheme to read a file and
catalog all discovered tokens. When the program runs to completion, it prints out
the total number of tokens read, as well as the five most common words.
"""

from sys import argv
# Filename should be the second argument, verify at least 2 arguments were
# passed and get the filename if there were.
if (len(argv)) == 2:
    filename = argv[1]
else:
    print("Usage: python3 pythonfile.py file_to_process.txt.")
    exit()
# A library to count the occurrences of words and an int to count the total
# number of words read. Example: {"word1": 1, "word2": 1, "word3": 2, ...}
wordcount = dict()
totalwords = 0

try:
    with open(filename, encoding="utf-8") as file:
        contents = file.read()
        words = contents.split()

        words = [word.lower() for word in words]

        # Loop to count totalwords.
        for word in words:
            totalwords += 1
            # Checks if word already exists and updates occurrence count.
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1


except FileNotFoundError:
    print(f"File '{filename}' not found. Please try again.")
    exit()

# Dictionary for organizing words into lists by the number of times they've occurred.

ranking = dict()
for word, count in wordcount.items():
    if count in ranking:
        ranking[count].append(word)
    else:
        ranking[count] = [word]

# Sort the lists of words in the ranking dictionary for consistency's sake.
for rank in ranking:
    ranking[rank] = sorted(ranking[rank])

# Create a list containing a tuple (count, word) for each of the words processed.
result = []


# Returns the first element in a tuple.
def get_count(tuple):
    return tuple[0]


# Loops through sorted list in descending order with highest occurrences first.
for count, word_list in sorted(ranking.items(), key=get_count, reverse=True):
    for word in word_list:
        result.append((count,word))

# Prints to display.
print(f"Total words read: {totalwords}")
for n in range(min(5, len(result))):
    print(f"The word '{result[n][1]}' occurred {result[n][0]} times.")

