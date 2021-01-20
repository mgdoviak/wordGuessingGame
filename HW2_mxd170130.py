# homework 2
# Mary Grace Doviak
import sys
import re
import random
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords

def driver(arg_input):
    # open and read file into raw_text
    file = open(arg_input)
    raw_text = file.read()
    # tokenize
    tokens = word_tokenize(raw_text)
    # calculate lexical diversity
    diversity = len(set(tokens)) / len(tokens)
    # f string makes it print to 2 decimals
    print("Lexical diversity: ", f'{diversity:.2f}')

    # call preprocess
    final_tokens, nouns = preprocess(raw_text)

    # create dictionary of nouns and their count
    noun_dict = {nouns[i] : final_tokens.count(nouns[i]) for i in range(0, len(nouns))}

    # create sorted dictionary and show 50 most common words
    dict1 = {}
    dict1 = sorted(noun_dict.items(), key = lambda x: x[1], reverse = True)
    print("50 most common words: ")
    common_words = []
    for x in range(50):
        temp = dict1[x]
        common_words.append(temp)
    for x in range(50):
        print(common_words[x])

    # make list of just common words
    common_list = []
    for i in common_words:
        temp = i[0]
        common_list.append(temp)

    # start guessing game
    score = 5
    word = random.choice(common_list)
    length = len(word)
    underscores = "_" * length

    print("Let's play a word guessing game!")
    print(underscores)

    # keep going until user has negative score
    while score >= 0:
        guess = input("Guess a letter: ")
        # if user inputs !
        if guess == "!":
            print("Sorry, you can't guess that! The word was ", word)
            break
        # if the user guesses a letter correctly
        if guess in word:
            for i in range(0, length):
                if guess == word[i]:
                    # print out updated underscores
                    underscores = underscores[:i] + guess + underscores[i + 1:]
            score += 1
            print("Right! Score is ", score)
            print(underscores)

        # if the user guesses a letter incorrectly
        if guess not in word:
            score -= 1
            print("Sorry, guess again. Score is ", score)
            print(underscores)

        # if user has negative points
        if score < 0:
            print("Sorry, you lost! The word was ", word)
            break

        # if user guessed all letters
        if "_" not in underscores:
            print("You solved it!")
            # get new word for user to guess
            word = random.choice(common_list)
            length = len(word)
            underscores = "_" * length
            print("Let's play again!")
            print("Current score is ", score)

# function to preprocess the raw text
def preprocess(raw_text):
    # convert to lowercase, get rid of non alpha characters
    # and tokenize
    alpha = re.sub(r'[.?!,$+=:;()\-\n\d]', ' ', raw_text.lower())
    tokens = word_tokenize(alpha)

    # get rid of stop words
    stop_words = set(stopwords.words('english'))
    no_stop = [w for w in tokens if not w in stop_words]

    # only keep words of > 5 length
    final_tokens = [w for w in no_stop if len(w) > 5]

    # lemmatize
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in final_tokens]

    # get rid of duplicates
    unique_lemmas = (set(lemmatized))

    # pos tagging
    tags = pos_tag(unique_lemmas)
    print("First 20 tagged words: ", tags[:20])

    # find nouns
    nouns = []
    nouns = [item[0] for item in tags if item[1][0] == 'N']
    print("nouns: ", nouns)

    print("Length of tokens after preprocessing: ", len(final_tokens))
    print("Length of nouns after preprocessing: ", len(nouns))

    return final_tokens, nouns


if __name__ == '__main__':
    # check system arguments
    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
        print('Input File: ', arg_input)
        driver(arg_input)
    else:
        print('File name missing')
    print('\nProgram ended')
