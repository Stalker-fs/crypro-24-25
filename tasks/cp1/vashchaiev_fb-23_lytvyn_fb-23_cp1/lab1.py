from math import log2
from sys import argv
import re

chk_alph = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
file_n = argv[1:][0]

def bigrams2csv(alphabet, bigrams, file_name):
    matrix = [[0 for _ in range(len(alphabet))] for _ in range(len(alphabet))]

    for key, val in bigrams.items():
        row = alphabet.index(key[0])
        column = alphabet.index(key[1])
        matrix[row][column] = val

    with open(file_name, "w") as t:
        t.write(' ;' + ';'.join(alphabet) + '\n')
        for r in matrix:
            t.write(alphabet[matrix.index(r)] + ';' + ';'.join(map(str, r)) + '\n')

def freq2csv(letters, f_name):
    sorted_letters = dict(sorted(letters.items(), key=lambda item: item[1], reverse=True))
    with open(f_name, "w") as t:
        t.write("symbol;frequency\n")
        for key, value in sorted_letters.items():
            t.write(f"{key};{value}\n")

# Підрахунок частот букв у тексті, де немає символів ".,!? "
# 1. частоти букв
def freq_symbols(gap):
    letters = dict()
    text_size = 0
    text = ""
    
    with open(file_n, "r", encoding="utf-8") as file:
        #for s in file.read().lower():
            # if s in chk_alph or (gap and s == " "):
            #     text += s
        content = file.read()
        content = content.lower()
        cleaned = re.sub(r'[^а-яё\s]+', '', content)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned if gap else cleaned.replace(" ", "")
        text = cleaned.strip()   

        for item in text:
            if item not in letters.keys():
                letters[item] = 1
            else:
                letters[item] += 1

        text_size = len(text)

    for key, val in letters.items():
        letters[key] = val / text_size
    return letters

#Підрахунок частот букв у тексті, де немає символів ".,!? "
# 2. Перехресні біграми
# 3. Не перехресні біграми
def bigrams(gap, cross):
    bigrams = dict()
    text = ""

    alph = chk_alph + ' ' if gap else chk_alph

    for i in alph:
        for j in alph:
            bigrams[i + j] = 0

    with open(file_n, "r", encoding="utf-8") as file:
        # for s in file.read().lower():
        #     if s in chk_alph or (gap and s == " "):
        #         text += s

        content = file.read()
        content = content.lower()
        cleaned = re.sub(r'[^а-яё\s]+', '', content)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned if gap else cleaned.replace(" ", "")
        text = cleaned.strip()   

        for i in range(0, len(text) - 1, 1 if cross else 2):
            item = text[i] + text[i + 1]
            if item in bigrams.keys():
                bigrams[item] += 1

        bigrams_count = sum(bigrams.values())
        # with open("gvedg.txt", "a") as l:
        #     l.write(f"\nПропуски: {gap} <-+-> Перехресно: {cross}")
        #     l.write(f"\nSum: {sum(bigrams.values())}\n")
        #     l.write('\n')
        #     for key, value in bigrams.items():
        #         l.write(f'{key}: {value}\n')
        #     l.write('-'*50)
        for key, val in bigrams.items():
            bigrams[key] = val / bigrams_count

    return bigrams

def entropy(bigrams, n = 1):
    return -sum(p * log2(p) for p in bigrams.values() if p > 0) / n

def redundancy(h, alphabet):
    return 1 - (h / log2(len(alphabet)))

# 1. частоти букв
letters_g = freq_symbols(True)
letters = freq_symbols(False)

# 2. Перехресні біграми
cross_bigrams_g = bigrams(True, True)
cross_bigrams = bigrams(False, True)

# 3. Не перехресні біграми
bigrams_g = bigrams(True, False)
bigrams = bigrams(False, False)

h1g = entropy(letters_g)
h1 = entropy(letters)
crh2g = entropy(cross_bigrams_g, 2)
crh2 = entropy(cross_bigrams, 2)
h2g = entropy(bigrams_g, 2)
h2 = entropy(bigrams, 2)
avg_entropy = (h1g + h1 + crh2g + crh2 + h2g + h2) / 6

print(f"{'Type of entropy':<40} {'Entropy':<25} {'Redundancy'}")
print("-" * 90)
print(f"{'H1':<40} {h1g:<25} {redundancy(h1g, chk_alph + ' ')}")
print(f"{'H1 without gaps':<40} {h1:<25} {redundancy(h1, chk_alph)}")
print(f"{'H2 cross bigrams':<40} {crh2g:<25} {redundancy(crh2g, chk_alph + ' ')}")
print(f"{'H2 cross bigrams without gaps':<40} {crh2:<25} {redundancy(crh2, chk_alph)}")
print(f"{'H2 bigrams':<40} {h2g:<25} {redundancy(h2g, chk_alph + ' ')}")
print(f"{'H2 bigrams without gaps':<40} {h2:<25} {redundancy(h2, chk_alph)}")
print("\nInfo")
print("-" * 50)
print(f"{'Max entropy' :<20} {log2(len(chk_alph))}")
print(f"{'AVG entropy':<20} {avg_entropy}")
print(f"{'Total redundancy':<20} {redundancy(avg_entropy, chk_alph)}")

# 7. Таблиці
freq2csv(letters_g, "Table1_freq_g.csv")
freq2csv(letters, "Table1_freq.csv")
bigrams2csv(chk_alph + ' ', cross_bigrams_g, "Table2_cross_bigrams_g.csv")
bigrams2csv(chk_alph, cross_bigrams, "Table2_cross_bigrams.csv")
bigrams2csv(chk_alph + ' ', bigrams_g, "Table2_bigrams_g.csv")
bigrams2csv(chk_alph, bigrams, "Table2_bigrams.csv")
