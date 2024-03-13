"""
Assignment 2: WordRank Enhanced
Author: Shanie Portal
Semester: Spring 2024
Description: This file implements a simple tokenizaiton scheme to read a file and
catalog all discovered tokens.
"""

from sys import argv
from sys import exit as sys_exit
from typing import List, Tuple

######################################################
## Globally available data structures and variables ##
######################################################
wordcount = {}
stopwords = {}
ranking = {}
NUM_WORDS_TO_PRINT = 10


######################
## Helper Functions ##
######################
def usage() -> None:
    """
    A convenience method to inform the user of how to directly run the module from a
    command line if they have provided the incorrect number of arguments.

    Raises:
      SystemExit() after printing usage
    """
    print("Direct usage: python word_rank.py file/at/path/to/process.txt.")
    sys_exit()

def isstopword(token: str) -> bool:
    """
    This convenience function tests to see whether the provided word is a stopword. A
    stopword is a word that does not add contextual value to a programmatic
    understanding of the topic of the text from which the word was extracted.

    Args:
      token: The incoming word to be checked

    Returns:
      True if the token is a stopword, otherwise False
    """
    _stopwords = frozenset(
        {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "but",
            "by",
            "for",
            "if",
            "in",
            "into",
            "is",
            "it",
            "no",
            "not",
            "of",
            "on",
            "or",
            "such",
            "that",
            "the",
            "their",
            "then",
            "there",
            "these",
            "they",
            "this",
            "to",
            "was",
            "will",
            "with",
        }
    )
    return token in _stopwords

def transform_word(token: str) -> str:
    """
    This function transforms the incoming word to prepare it for storage. There are four
    transformations applied:
      1. Leading/trailing whitespace is removed
      2. The word is converted to all lowercase letters
      3. All instances of an apostrophe followed by an s at the end of the word are
         removed. This is done to eliminate possessive forms of words.
      4. All remaining punctuation is removed from anywhere in the word. See
         https://www.geeksforgeeks.org/python-remove-punctuation-from-string/ or
         https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

    Args:
      token: The incoming raw token to be transformed into a "word"

    Returns:
      The transformed token, now suitable for storage
    """
    # String initialized with all possible punctuation.
    puncList = r'''!()-[]{};:'"“”\,<>./?@#$%^&*_~'''

    # Removing whitespaces and transforming to lowercase.
    token = token.strip()
    token = token.lower()

    # Remove all punctuation.
    for ele in token:
        if ele in puncList:
            token = token.replace(ele, "")

    # Return token.
    return token

def store_word(token: str) -> bool:
    """
    Given a word token, place it into the correct data structure and return True. Empty
    strings are not processed and False is returned.

    Args:
      token: The incoming word that needs to be stored

    Returns:
      True if the word was non-empty, False otherwise
    """
    # Test if token exists, or return False.
    if token:
        # Update token count in dictionary or set to 0 if not present, then return True.
        if not isstopword(token):
            wordcount[token] = wordcount.get(token, 0) + 1
        else:
            stopwords[token] = stopwords.get(token, 0) + 1
        return True
    return False


def parse(filename: str) -> int:
    """
    Extract tokens from the requested file resource by first attempting to open the
    file, retrieving a line of text, splitting it into separate words, storing each word
    using the store_word function, and incrementing num_words when the result of
    `store_word` is True. Be sure to account for the possibility of the file not being
    found and print, f"File '{filename}' not found. Please try again." if the file open
    operation fails, then call sys_exit(). If the operations succeed, when the entire
    file is processed return num_words.

    Args:
      filename: The path/name of the file to extract from

    Raises:
      SystemExit() if file not found
    """

    num_words = 0

    # Open the file, tokenize its content, transform each word, and store it.
    try:
        with open(filename, encoding="utf-8") as file:
            while text := file.readline():
                words = text.split()
                for word in words:
                    # Transform word and increase the count.
                    transformed_word = transform_word(word)
                    num_words += 1
                    # Store the word.
                    store_word(transformed_word)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please try again.")
        sys_exit()

    return num_words

def rank() -> None:
    """
    Create word rankings by inverting the `word->count` mapping to be of the form
    `count->[word1, word2, ...]`
    """

    # Create a ranking dictionary based on word counts.
    for word, count in wordcount.items():
        if ranking.get(count):
            ranking[count].append(word)
        else:
            ranking[count] = [word]

def create_printable_list_of_tuples() -> List[Tuple[int, str]]:
    """
    Convert the ranked words into a list of tuples of the form (count, word), then sort
    the list in reverse order using the 0th index of each tuple to place the largest
    counts at the front of the list for easy printing.

    Guidance:
    For this effort it's helpful to understand how the built in python sort works.

    First, the python static function, `sorted`, and list member function, `sort`, are
    stable. This means that if two items were considered equal by the sort comparator
    they will be in the same order after the sort is performed.

    Second, the built in sort functions can take an argument for a function that
    consumes the current object being compared and returns a value that should be used
    for making the comparison. This function can be specified by 'key=(function)'.

    Third, there's a second argument that can be made that reverses the sort order, it
    can be specifed by 'reverse=(boolean value)'. Information on the list sort function
    is here: https://docs.python.org/3/library/stdtypes.html#list.sort. A second thing
    to consider to this end is the lambda expression, which you can read about here:
    https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions. These
    expressions can be conveniently used for things like the key of sort, if you don't
    want the sort to use the default comparison behavior.
    """

    # Convert ranking dictionary to a sorted list of tuples and return it.
    result = []
    for count, word_list in ranking.items():
        for word in word_list:
            result.append((count, word))
    result.sort(reverse=True)

    return result

def print_top_n_words(total_words: int, result: List[Tuple[int, str]]) -> None:
    """
    Use the constructed, ordered list of tuples to print out the top NUM_WORDS_TO_PRINT.

    Args:
      total_words: The total number of words/tokens that were encountered
      result: An ordered list of tuples in the form (count, word) for printing. Higher
              counts should appear at the front of the list.
    """
    print(f"Total words read: {total_words}")
    for n in range(min(NUM_WORDS_TO_PRINT, len(result))):
        print(f"The word '{result[n][1]}' occurred {result[n][0]} times.")

def run(filename: str) -> None:
    """
    This function is an orchestrator, invoking the necessary helper functions to execute
    this script as a standalone module.

    Args:
      filename: The file path/name to be processed

    Raises:
      SystemExit() if file not found
    """

    # Open and parse the file.
    total_words = parse(filename)
    # Order based on occurrences.
    rank()
    # Create printable version and print.
    final = create_printable_list_of_tuples()
    print_top_n_words(total_words, final)


##################################################
## What to do if invoked as a standalone script ##
##################################################
if __name__ == "__main__":
    ## Ensure filename provided or exit
    if len(argv) != 2:
        usage()

    ## Extract filename and pass along to orchestrator
    run(argv[1])
