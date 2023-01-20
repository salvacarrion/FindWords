# FindWords

Find words in a dictionary, following a pattern.
The goal of this project is to find mnemotecnic rules easily to remember words, sentences, or even numbers.

## Usage

There are 2 modes, with 2* options each:
- **Sequential:** Find words that match your pattern in order: (zpt → "...z...p...t...")
  - **With extra vowels:** (zpt → zapata, zapatear, zapato,...)
  - **With NO extra vowels:** Checks if the word exists
- **Permutation**: Find anagrams for your pattern: (zpt → zpt, ztp, pzt, ptz, tzp, tpz)
  - **With extra vowels:** (zpt → zapato, topaz, potazo,...)
  - **With NO extra vowels:** Checks if your word is an anagram of another. (mrao -> roma, mora, amor, ramo,...)

> **PRO TIP:** The **most useful modes** are:
> - **Sequential with extra vowels:** To find words matching the pattern
> - **Permutation with NO extra vowels:** To find anagrams of the pattern


###  Examples: Sequential + Extra vowels
```python
$python find_words.py
Loading words...
Building dataset...
Preservar el orden de las letras? (y/n) [n]: >? y
Se pueden añadir vocales adicionales? (y/n) [n]: >? y
Introduce las letras a buscar: >? zptd
zapatead
zapateado
zapateador
zapateadora
zapatuda
zapatudo
--------------------------------------------------
- Patrón buscado: zptd
- Total palabras encontradas: 6
- Tiempo de ejecución: 0.562 segundos
```


###  Examples: Anagram + With NO extra vowels
```python
Loading words...
Building dataset...
Preservar el orden de las letras? (y/n) [n]: >? 
Se pueden añadir vocales adicionales? (y/n) [n]: >? 
Introduce las letras a buscar: >? mrao
amor
armo
armó
maro
mora
morá
ramo
roma
--------------------------------------------------
- Patrón buscado: mrao
- Total palabras encontradas: 8
- Tiempo de ejecución: 0.356 segundos
```
