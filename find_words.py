import time
import os

URL_DICTIONARY = "https://github.com/JorgeDuenasLerin/diccionario-espanol-txt/raw/master/0_palabras_todas.txt"


def remove_accents(word):
    """
    This function removes the accents from a word.
    """
    # Create a dictionary that maps the accents to the letters without accents
    accents_dictionary = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ü': 'u',
        'ñ': 'n',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'Ü': 'U',
        'Ñ': 'N'
    }
    
    # Create a list of the letters of the word
    letters = list(word)
    
    # Replace the letters with accents with the letters without accents
    for i in range(len(letters)):
        if letters[i] in accents_dictionary:
            letters[i] = accents_dictionary[letters[i]]
    
    # Return the word without accents
    return ''.join(letters)

def remove_diacritics(word_without_accents):
    """
    This function removes the diacritics from a word.
    """
    # Create a list of the letters of the word
    letters = list(word_without_accents)
    
    # Replace the letters with diacritics with the letters without diacritics
    for i in range(len(letters)):
        if letters[i] == '¿':
            letters[i] = 's'
        elif letters[i] == '¡':
            letters[i] = 'i'
    
    # Return the word without diacritics
    return ''.join(letters)

def remove_vowels(word_without_accents):
    """
    This function removes the vowels from a word.
    """
    # Create a list of the letters of the word
    letters = list(word_without_accents)
    
    # Replace the vowels with the letters without vowels
    for i in range(len(letters)):
        if letters[i] in 'aeiouAEIOU':
            letters[i] = ''
    
    # Return the word without vowels
    return ''.join(letters)

def get_missing_vowels(word):
    vowels = 'aeiou'
    missing_vowels = ''
    for vowel in vowels:
        if vowel not in word:
            missing_vowels += vowel
    missing_vowels = set(missing_vowels)
    return missing_vowels

def load_words(file_name):
    # Open the file and load the words into a list
    with open(file_name) as file:
        words = file.read().split()
    return words

def build_dataset(words):
    # Create a list of words without accents, diacritics and the given vowels
    words_without_accents = []
    for word in words:
        word_cleaned = word.lower().strip()
        word_cleaned = remove_accents(word_cleaned)
        word_cleaned = remove_diacritics(word_cleaned)

        # Add cleaned word to list
        words_without_accents.append(word_cleaned)
    
    # Create a dictionary that maps words without accents to a list of the words that have them
    words_dictionary = {}
    for i in range(len(words_without_accents)):
        if words_without_accents[i] in words_dictionary:
            words_dictionary[words_without_accents[i]].append(words[i])
        else:
            words_dictionary[words_without_accents[i]] = [words[i]]
    return words_dictionary
        
def find_words(letters, words_dictionary, ignore_all_vowels=False, preserve_order=False):
    # Make letters lowercase, remove accents and diacritics
    letters = letters.lower().strip()
    letters = remove_accents(letters)
    letters = remove_diacritics(letters)

    # Get missing vowels
    if ignore_all_vowels:
        vowels2remove = set('aeiou')
    else:
        vowels2remove = get_missing_vowels(letters)

    # Find all words in the dictionary whose key is a permutation of the given letters
    matched_words = []
    for key in words_dictionary:
        # Remove vowels from key (keeping order of the chars)
        new_key = [char for char in key if char not in vowels2remove]
        new_key = ''.join(new_key)

        # Check if the new_key is a permutation of the given letters
        word = words_dictionary[key]
        if preserve_order and (new_key == letters):
            matched_words += word
        elif not preserve_order and (sorted(new_key) == sorted(letters)):
            matched_words += word
        else:
            pass
    
    return matched_words

def download_file(url, path):    
    # Download file form URL
    import requests
    r = requests.get(url)

    # Save file
    with open(path, 'wb') as file:
        file.write(r.content)  

if __name__ == '__main__':
    print("Loading words...")

    # Check if the dictionary exists, else, download it
    file_name = os.path.join(os.path.dirname(__file__), 'words.txt')
    if not os.path.exists(file_name):
        print("Dictionary not found. Downloading dictionary...")
        download_file(URL_DICTIONARY, file_name)

    # Load words
    words = load_words(file_name=file_name)

    print("Building dataset...")
    words_dictionary = build_dataset(words=words)
    
    # Ask if vowels should be ignore
    ignore_all_vowels = input('¿Ignorar todas las vocales? (y/n): ').lower().strip() == 'y'
    preserve_order = input('¿Preservar el orden de las letras? (y/n): ').lower().strip() == 'y'

    # Get the letters from the user
    while True:
        letters = input('Introduce las letras a buscar: ')

        # Find words
        start_time = time.time()
        matched_words = find_words(letters, words_dictionary, ignore_all_vowels, preserve_order)
        end_time = time.time()

        # Print the list of words (one per line)
        for word in matched_words:
            print(word)

        # Summary
        print('-' * 50)
        print(f'- Palabra buscada: {letters}')
        print(f'- Total palabras encontradas: {len(matched_words)}')
        print(f'- Tiempo de ejecución: {end_time - start_time:.3f} segundos')
        print('')

    
