# Kasiski
Python script that breaks Vigenere cipher in spanish by using the Kasiski method

This method automatizes the Kasiski attack to the Vigenere cipher for texts ciphered in Spanish. (https://www.youtube.com/watch?v=K3tpKeDQs6s)

## How does the program work
*  Estimates key length by getting the 5 most common N-Grams. As the key repeats every L positions (where L is the key length), its very likely that if several N-Grams are repeated twice or more, the gcd of their separations equals to L. If the script gets a gcd equal to 1 (which means a key length of 1, something really unlikely in Vigenere Cipher), it will repeat the procedure but getting the 4, 3, 2 and 1 most common N-Grams (instead of 5) until the gcd is different from 1.
*  Divides the text in L subcriptograms (criptograms 1,2,...,L are ciphered with the letters 1,2,...,L of the key). For instance, if our ciphered text is "ILOVECRIPTOGRAPHY" and our estimated key length is 3, the division will result in: 'IVRTRH', 'LEIOAY', 'OCPGP'
*  As every subcryptogram is ciphered with the same key letter, we have L texts ciphered with a monoalphabetic cipher of key length 1 (which means that each letter is displaced N positions). Thus, the [frecuency of letters in spanish](https://es.wikipedia.org/wiki/Frecuencia_de_aparición_de_letras) is mantained on each of them.
*  For each subcryptogram, the program will compute which letter in the ciphered text maps to the letter 'A' in the clear text. If in subcryptogram N the letter 'A' was ciphered into letter 'T' (for example), it means that the key's letter in position N is "T" (A + T mod 26 = T)
*  To get which letter maps to letter 'A' in each subcryptogram, the program gets the 6 most common letters on each of them. It assumes that letters A, E, O, S (whose frecuencies in spanish are [0.1314, 0.1314, 0.0916, 0.0782]) will be among the 6 most common. For each subcryptogram, 6 vectors will be computed, each one containing one possible array of AEOS frecuencies. On the first vector it is assumed that letter A is the most common one (so letter 'E' has to be 4 letters ahead of letter 'A', letter 'O' 10 letters ahead of letter 'E' and letter 'S' 4 letters ahead of letter 'O'), on the second vector it is assumed that letter 'A' is the second most common one, on the third vector it is assumed that letter 'A' is the third most common one, etc. For each of the 6 vectors, the Euclidean Distance with vector [0.1314, 0.1314, 0.0916, 0.0782] will be computed, getting the one with less value.
*  Once the above step is repeated on each subcryptogram, the program will know wich letter maps to 'A' on each subcriptogram, therefore knowing the key. For instance, if the ciphered text was divided in 5 cryptograms, and the letters into which 'A' was ciphered were ['W', 'O', 'R', 'L', 'D'], the key will be "WORLD"

## Preconditions
*  The original text must have been written in spanish (but adapting the script to other languages is really simple)
*  The original text must have been written in ASCII characters (with no Ñ)
*  The ciphered text must not have blank spaces (inserting a method that trims the text before passing it to the algorithm will solve this problem)

## Example of execution
```bash
$ python3 kasisky.py encryptedFile.encrypted
Key length: 7
Most probable key: BOTNETS
-------
MESSAGE
-------
THISISAMESSAGEENCRYPTEDUSINGVIGENERECIPHERINVENTEDINXVICENTURYITWASFORYEARSDESCRIBEDASTHEINDECIPHERABLEFIGURE...
```
