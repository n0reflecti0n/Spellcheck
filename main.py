import collections
import time


def tri_grams(word):
    word = "${}$".format(word)
    w_l = len(word) + 1
    return [word[i:i + 3] for i in range(0, max(w_l - 3, 1))]


def find_candidates(word, dict_kgrams):
        word_kgrams = tri_grams(word)
        word_freq = collections.Counter()
        for g in word_kgrams:
            index = dict_kgrams.get(g)
            if index is not None:
                for x in index:
                    word_freq[x] += 1
        return word_freq.most_common(4096)


def generate_kGramm_index(dictionary):
    kgram_index = {}
    for i, word in enumerate(dictionary):
        splitted = tri_grams(word)
        for kgram in splitted:
            kgram_in_index = kgram_index.get(kgram)
            if kgram_in_index is not None:
                kgram_in_index.append(i)
            else:
                kgram_index[kgram] = [i]
    return kgram_index


def levenstein(str1, str2):
    N = len(str1) + 1
    M = len(str2) + 1
    matrix = [[0] * M for _ in range(N)]
    for i in range(N):
        matrix[i][0] = i
    for j in range(M):
        matrix[0][j] = j
    for i in range(1, N):
        for j in range(1, M):
            matrix[i][j] = min(matrix[i][j - 1] + 1,
                               matrix[i - 1][j] + 1,
                               matrix[i - 1][j - 1] +
                               (str1[i - 1] != str2[j - 1]))
    return matrix[N - 1][M - 1]


def top_similar(dict, str, top):
    most_similar = []
    for i, word in enumerate(dict):
        distance = levenstein(word, str)
        if i < top:
            most_similar.append((word, distance))
        elif most_similar[-1][1] > distance:
            most_similar[-1] = (word, distance)
        most_similar = sorted(most_similar, key=lambda x: x[1])
    return most_similar


with open("russian_dictionary.txt") as file:
    words = file.read().split()
    dict_kgrams = generate_kGramm_index(words)
word = '_'
while True:
    print('Введите слово с опечаткой:')
    word = input()
    if word == '':
        break
    t = time.time()
    temp = find_candidates(word, dict_kgrams)
    print('Возможные варианты:')
    for x, y in top_similar([words[i[0]] for i in temp], word, 10):
        print(x)
    print(time.time() - t)
    print('-------------------------------')
