# Created by Paulo Seoane Davila in 2020

import re
import sys
from functools import reduce
from fractions import gcd	
from math import sqrt

def readFile(name):
	f = open(name)
	content = f.read()
	f.close()
	return content

"""
Returns the euclidean distance from the frecuency of the letters AEOS to the frecuency of
these letters in Spanish
---------------
Input:
aeosFrecuencies: [Float]
Output:
Distance: Float
"""
def distanceToNormalFrencuencies(aeosFrecuencies):
	normalFrecuencies = [0.1314, 0.1314, 0.0916, 0.0782]
	sum = 0
	for i in range(0, 4):
		sum += (normalFrecuencies[i] - aeosFrecuencies[i])**2
	return sqrt(sum)


"""
Input:
baseKey: String
length: Int. Represents the length of the output key
---------------
Output:
key: [char]
---------------
Usage example:
generateKey("dog", 4) = ["d", "o", "g", "d"]
"""
def generateKey(baseKey, length):
	baseKeyLength = len(baseKey)
	key = [baseKey[i % baseKeyLength] for i in range(0, length)]
	return key

"""
Deciphers a message using the Vigenere Algorithm: M[i] = (C[i] - K[i] + 26) % 26
Input:
message: String
key: String
---------------
Output:
Deciphered message: String
---------------
Usage example:
decipher("FCGURWQOVDG", "DOS") = "COORDENADAS"
"""
def decipher(message, key):
	messageLength = len(message)
	decipheredMessage = ""
	keyArray = generateKey(key, messageLength)
	for i in range(0, messageLength):
		decipheredNumber = (ord(message[i]) - ord(keyArray[i]) + 26) % 26
		decipheredMessage += chr(decipheredNumber + 65)
	return decipheredMessage

#Precondition: Capital letter
"""
Returns the letter that results from adding n to the input letter
--------------
Input:
letter: String. A char in the range [A-Z]
n: Int. Number that's going to be added to the letter
---------------
Output:
resultChar: Char
---------------
Example:
addToLetter("A", 4) = 'E'
"""
def addToLetter(letter, n): 
	positionInAlphabet = ord(letter) - 65
	newLetter = (positionInAlphabet + n) % 26
	return chr(newLetter + 65)

#Returns a list of tuples in the following format: [(nGram, repetitions)]
"""
Returns an ordered list of touples representing, from greatest to lowest, all
the nGrams found in the text and their number of repetitions
---------------
Input:
text: String. The text to analyze
n: Int. The length of the n-grams
---------------
Output:
nGrams: [(String, Int)]
---------------
Example:
getNGrams("ABCDEFABC", 3) = [("ABC", 2), ("DEF", 1)]
"""
def getNGrams(text, n): 
	regex = f".\x7B{n}\x7D"
	matches = re.findall(regex, text)
	nGrams = dict({})
	for match in matches:
		if match in nGrams:
			nGrams[match] = nGrams[match] + 1
		else:
			nGrams[match] = 1
	return sorted(nGrams.items(), key=lambda x: x[1], reverse=True)

"""
Returns all the indexes where a certain nGram ends in a given text
---------------
Input:
nGram: String. Regular expression of the nGram
text: String. The text in which to look for ocurrences
---------------
Output:
Positions: [Int]
"""
def getNGramPositions(nGram, text):
	matches = re.finditer(nGram, text)
	positions = []
	for match in matches:
		positions.append(match.end(0))
	return positions

"""
We are going to get the 5 most common substrings: N tetragrams repeated 2 or more times
(at most 5) and 5 - N trigrams repeated more than 2 times 
"""
"""
Estimates the key length given a text. For that purpose, it gets the X most common N-Grams
and computes the gcd of their separations. 
It begins trying to get the 5 most common tetragrams that are repeated more than twice,
if there are less than five, it will get X - 5 trigrams, being X the number of tetragrams
got.
In case the gcd of the 5 most common N-Grams returns 1, the function will repeat the
above procedure getting the 4, 3, 2 and/or 1 most common n-grams, until the gcd is different
from 1 or it reaches 1 n-gram
---------------
Input:
cipheredText: String
---------------
Output:
keyLength: int
"""
def estimateKeyLength(cipheredText):
	def estimateKeyLength(cipheredText, maxSamples):
		tetraGrams = getNGrams(cipheredText, 4)
		triGrams = getNGrams(cipheredText, 3)
		positions = []
		i = 0
		j = 0
		while len(positions) < maxSamples: 
			if tetraGrams[i][1] >= 2:
				positions.append(getNGramPositions(tetraGrams[i][0], cipheredText))
				i+=1
			elif triGrams[i][1] >= 2:
				positions.append(getNGramPositions(triGrams[j][0], cipheredText))
				j+=1
			else:
				break
		differences = []
		for pos in positions:
			differences += [y - x for x, y in zip(pos, pos[1:])]
		return reduce(gcd, differences)

	keyLength = 1
	maxSamples = 6
	while (keyLength == 1 and maxSamples > 1):
		maxSamples -= 1
		keyLength = estimateKeyLength(cipheredText, maxSamples)
	return keyLength

"""
Divides a string into keyLength substrings
---------------
Input:
keyLength: Int
text: String
---------------
Output:
subcriptograms: [[String]]
"""
def getSubcriptograms(keyLength, text):
	textLength = len(text)
	return [text[i:textLength:keyLength] for i in range(0, keyLength)]

"""
Returns the frecuencies of the input letters in a given text
---------------
Input:
letters: [String]. The letters to calculate the frecuency from
text: String
Output:
frecuencies: [Float]: The frecuencies of the letters in the input array
"""
def getLettersFrecuency(letters, text):
	criptogramLength = len(text)
	lettersDictionary = dict(getNGrams(text, 1)) #Dictionary [letter:repetitions].
	frecuencies = []
	for letter in letters:
		if not (letter in lettersDictionary):
			frecuencies.append(0)
		else:
			frecuencies.append(lettersDictionary[letter] / criptogramLength)
	return frecuencies

"""
Gets the key based on the keyLength, dividing the text on keyLength
substrings and applying to each one the AEOS procedure.
---------------
Input:
keyLength: Int
cipheredText: String
---------------
Output:
key: String
"""
def getKey(keyLength, cipheredText):
	criptograms = getSubcriptograms(keyLength, cipheredText)
	print(keyLength)
	possibleKey = []
	for criptogram in criptograms:
		#AEOS rule
		letters = getNGrams(criptogram, 1) #Ordered list of letters and their repetitions
		distances = []
		for i in range(0, 6): #We assume that AEOS will be among the 6 most common 
			possibleA = letters[i][0]
			possibleE = addToLetter(possibleA, 4)
			possibleO = addToLetter(possibleE, 10)
			possibleS = addToLetter(possibleO, 4)
			possibleAEOS = [possibleA, possibleE, possibleO, possibleS]
			frecuencies = getLettersFrecuency(possibleAEOS, criptogram)
			distances.append((possibleA, distanceToNormalFrencuencies(frecuencies)))
		sortedDistances = sorted(distances, key=lambda x: x[1])
		possibleKey.append(sortedDistances[0][0])
	return possibleKey

def usage():
	return """
	Usage:
	vigenere.py <textFile>
	"""

def printResults(keyLength, key, message):
	print(f"Key length: {keyLength}")
	print(f"Most probable key: {key}")
	print("-------")
	print("MESSAGE")
	print("-------")
	print(message)	

def main():
	if len(sys.argv) != 2:
		return print(usage())
	else:
		cipheredText = readFile(sys.argv[1]).upper()
		keyLength = estimateKeyLength(cipheredText)
		keyLetters = getKey(keyLength, cipheredText)
		if keyLetters == []:
			print("Unable to decrypt message")
			exit(1)
		key = reduce(lambda x,y: x+y, keyLetters) #["C", "A", "T"] -> "CAT"
		message = decipher(cipheredText, key)
	printResults(keyLength, key, message)

main()
