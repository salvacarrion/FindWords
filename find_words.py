import time
import os
import re
from collections import OrderedDict

# Check if requests package is installed, else raise an error
try:
    import requests
except ImportError:
    raise ImportError('The requests package is not installed. Please install it with "pip install requests".')

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


def build_dataset(word_list):
    # Create a list of words without accents, diacritics and the given vowels
    words_without_accents = []
    for w in word_list:
        word_cleaned = w.lower().strip()
        word_cleaned = remove_accents(word_cleaned)
        word_cleaned = remove_diacritics(word_cleaned)

        # Add cleaned word to list
        words_without_accents.append(word_cleaned)

    # Create a dictionary that maps words without accents to a list of the words that have them
    words_dictionary = {}
    for i in range(len(words_without_accents)):
        if words_without_accents[i] in words_dictionary:
            words_dictionary[words_without_accents[i]].append(word_list[i])
        else:
            words_dictionary[words_without_accents[i]] = [word_list[i]]
    return words_dictionary


def find_words(pattern, words_dictionary, preserve_order=False, allow_extra_vowels=False):
    # Clean pattern
    pattern = pattern.lower().strip()
    pattern = remove_accents(pattern)
    pattern = remove_diacritics(pattern)

    # Build pattern to ignore vowels
    new_pattern = ''
    if allow_extra_vowels:
        # Create a regular pattern where the missing vowels are optional
        for letter in pattern:
            new_pattern += '[aeiou]*' + letter
        new_pattern += '[aeiou]*'

    # Find words that match the pattern
    matched_words = []
    for clean_word in words_dictionary:
        if preserve_order:
            if allow_extra_vowels:  # Useful when the pattern has no vowels, else, tricky
                # Check if the clean word matches the pattern
                if re.match(new_pattern, clean_word):
                    # Add the words to the tmp ist
                    matched_words += words_dictionary[clean_word]

            else:  # Dummy case
                if clean_word == pattern:
                    matched_words += words_dictionary[clean_word]

        else:  # Permutations
            if allow_extra_vowels: # Not very useful
                missing_vowels = get_missing_vowels(pattern)

                # Remove the missing vowels from the clean word
                tmp_clean_word = [letter for letter in clean_word if letter not in missing_vowels]

                # Check if both words contain the same letters (excluding the missing vowels)
                if set(tmp_clean_word) == set(pattern):
                    matched_words += words_dictionary[clean_word]
            else:  # Definetly useful
                if sorted(clean_word) == sorted(pattern):
                    matched_words += words_dictionary[clean_word]
    return matched_words


def download_file(url, path):
    # Download file form URL
    r = requests.get(url)

    # Save file
    with open(path, 'wb') as file:
        file.write(r.content)


if __name__ == '__main__':
    print("Loading words...")

    # Check if the dictionary exists, else, download it
    file_name = os.path.join(os.path.dirname(__file__), 'data/words.txt')
    if not os.path.exists(file_name):
        print("Dictionary not found. Downloading dictionary...")
        download_file(URL_DICTIONARY, file_name)

    # Load words
    word_list = load_words(file_name=file_name)

    print("Building dataset...")
    words_dictionary = build_dataset(word_list=word_list)

    # Ask for settings (with default value)
    preserve_order = (input("Preservar el orden de las letras? (y/n) [n]: ").lower().strip() or 'n') == 'y'
    allow_extra_vowels = (input("Se pueden añadir vocales adicionales? (y/n) [n]: ").lower().strip() or 'n') == 'y'

    # Get the letters from the user
    while True:
        pattern = input('Introduce las letras a buscar: ')

        # Find words
        start_time = time.time()
        matched_words = find_words(pattern, words_dictionary, preserve_order, allow_extra_vowels)
        end_time = time.time()

        # Print the list of words (one per line)
        for word in matched_words:
            print(word)

        # Summary
        print('-' * 50)
        print(f'- Patrón buscado: {pattern}')
        print(f'- Total palabras encontradas: {len(matched_words)}')
        print(f'- Tiempo de ejecución: {end_time - start_time:.3f} segundos')
        print('')
