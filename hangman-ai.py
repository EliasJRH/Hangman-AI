#add any global variables your AI needs here:
word_length = 0
#wordlist is all possible words the game could pick as a puzzle
#it is only initialized when your module is imported, so do not change it
wordlist = [] 
refined_list = [] # list that holds all the words that the word could be, keeps getting refined as the game progresses
known_letters = [] # a list of known letters and their indexes in the word
guessed_letters = [] # a list of letters that have been guessed
last_letter = "" # variable to hold the last letter guess

#letters is a list of all characters your program could guess
#it is re-initialized each round, so you can modify it
letters = []
filein = open("base-words.txt", "r")
wordlist = filein.read().lower().split("\n")
filein.close();

#round initialization
#this is called at the start of each round
#the input string is a single _ for each character in the puzzle
def initround(string):
	#initializes the list of letters that could be guessed
	#you can use this list in your AI implementation if desired
    global refined_list # global declarations making sure that this function always references them
    global known_letters
    global guessed_letters
    global last_letter
    word_length = len(string) # gets the length of the word from the passed in string argument
    refined_list.clear() # clears all of the lists
    known_letters.clear()
    guessed_letters.clear()
    last_letter = "" # clears the variable
    letters.clear()
    for i in range(ord('a'), ord('z')+1):
        letters.append(chr(i))
    for word in wordlist: # Creates a refined list of words that only have the same amount of characters as the word that was chosen
        if len(word) == word_length:
            refined_list.append(word)
	#add any more initialization code your AI requires here
	#...	


def refineguess(string): # function that culls our refined words list
    global refined_list # gets the global refined list
    word_accepted = True # boolean to check if the word is accepted
    for index in range(len(string)): # takes the string that was returned from each guess and further refines it to words only containing letters at specific indexes
        if string[index] != '_' and ((string[index], index)) not in known_letters:
            # if each character in the currently guessed word has been guessed and had not already been recorded in the known_letters list
            known_letters.append((string[index], index)) # adds a tuple containing the letter and its index to the list
    for known in known_letters: # for every known pair in the known letters list
        p = 0 # pointer variable, makes deleting words easier
        while True: # while loop that will continue to run until our pointer has reached the end of the list
            length = len(refined_list) # continuously getting the length of the refined list after it keeps getting deleted
            if p == length: #checks if the pointer is at the end, breaks out of the loop if true
                break
            if refined_list[p][known[1]] != known[0]:
                # if the character at the known index of a key pair is not the same as the character in the pair
                del refined_list[p]
                # delete that word from the list
                # example: correct word is apple, program has guessed 'a', therefore known list has key pair ('a',0)
                # if the word that we are examining is 'blues', the program checks if the first character is equal to 'a'
                # it's not, so that word gets deleted
            else: 
                #otherwise, if it passes the check, increase the pointer by 1
                p += 1
    return refined_list # return the new refined list
    
def removewrongwords(guessed_letter): # function to remove any word that cannot be the word
    global refined_list # gets the global refined list
    if guessed_letter != "": # when the guessed letter isnt empty (beginning of game)
        p = 0 # create a pointer variable
        while True: # while True to run through absolutely every word in the refined list
            length = len(refined_list) # repeatedly getting the length of the list because it keeps shrinking
            if p == length: # once the pointer has reached the end of the list the loop breaks
                break
            if guessed_letter in refined_list[p]: # if the guessed letter is in the current word 
                del refined_list[p] # delete it
            else:
                p += 1 # otherwise, move the pointer up 1
    return refined_list # return the refined list
    
def finishword(word, string, guessed_letters): # function to send the remaining letters
    # takes in the last word in the refined list, the string containing the word to guess and a list of the guessed words
    for x in range(len(string)): # for every character in the unguessed string
        if string[x] == '_': # if the letter hasn't been guessed
            guessed_letters.append(word[x])
            return word[x] # guess the letter at the same index of the known word

def getmostfreqletter(guessed_letters_list): # function to retrieve the most common letter in all of the words
    letterfreq = { # creates a dictionary of every letter in the alphabet
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0,
        'h': 0,
        'i': 0,
        'j': 0,
        'k': 0,
        'l': 0,
        'm': 0,
        'n': 0,
        'o': 0,
        'p': 0,
        'q': 0,
        'r': 0,
        's': 0,
        't': 0,
        'u': 0,
        'v': 0,
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }
    for word in refined_list: # for every word in the refined list, then for every letter in the word
        for char in range(len(word)):
            letterfreq[word[char]] += 1 # increase the count of that letter by 1
    for letter in guessed_letters_list: # for every letter in the list of letters that has already been guessed
        letterfreq.pop(letter, None) # remove it from the dictionary
    vals = list(letterfreq.values()) # gets a list of values from the dictionary
    ks = list(letterfreq.keys()) # gets a list of keys from the dictionary
    return ks[vals.index(max(vals))] # returns the max value from the index
    # retrieves max value in value list, get the index of that value, returns with key[value]

#Add your AI code to guess a letter here
#The input string is the current puzzle, with _ for any unguessed letters
#You should output one lower-case character
def makeguess(string):   
    global last_letter # gets the global values of the variables and lists 
    global refined_list
    global guessed_letters
    guessed_letters.append(last_letter) # adds the last letter guessed to list of guessed letters
    letter_found = False # boolean to figure out if the letter that was guessed exists in the word
    if len(refined_list) > 1 and last_letter != "": # if the length of our refined list is greater than one or the last letter guessed is not blank (beginning of game)
        # if the length of the refined list is greater than one, then the program has not found the word yet, and has to keep searching
        for x in string: # for every character in the string
            # if the last letter that was guessed is in the string, the boolean changes to true meaning that our letter was correct
            if x == last_letter:
                letter_found = True
                break
        if not letter_found: # if the letter was not found
            refined_list = removewrongwords(last_letter) # set our refined list to be changed by removing every word that contains the incorrect guessed letter
        else:
            refined_list = refineguess(string) # this call to refineguess, removes every word that does not have matching letters at certain indexes
        last_letter = getmostfreqletter(guessed_letters) # the last letter variable gets set to the most frequent letter in our remaining list of words
        return last_letter # returns the last letter
    else: # otherwise, if there is only one word left in the refined words list, that means we found the word
       # function calls to send the remaining letters
       last_letter = finishword(refined_list[0], string, guessed_letters)
       return last_letter 


