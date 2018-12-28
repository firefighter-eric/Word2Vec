import re
import pickle


class Data:
    def __init__(self):
        self.id = None
        self.case = None
        self.penalty = None
        self.laws = list()


def readfile(filename='train.txt', line_num=4e4):
    with open(filename, 'r') as file:
        data = list()
        i = 0
        for line in file:
            if i > line_num:
                break
            i += 1
            line = line.strip().split('\t')
            data.append(Data())
            data[-1].id = int(line[0])
            data[-1].case = line[1]
            data[-1].penalty = int(line[2])
            for n in line[3].split(','):
                data[-1].laws.append(int(n))
    return data


def text_init(data):
    text = list()
    for d in data:
        for t in re.split('，|。|：|；|（|）|！|？|、', d.case):
            text.append(list(t))
    return text


class Word:
    def __init__(self):
        self.li = list()
        self.count = dict()
        self.serial = dict()

    def add_word(self, new_word):
        self.li.append(new_word)
        self.count[new_word] = 0
        self.serial[new_word] = self.li.index(new_word)


def words_counting(texts):
    words = Word()
    for text in texts:
        for _word in text:
            words.count[_word] = words.count.get(_word, 0) + 1

    DELTA_COUNT = 2
    for word, count in words.count.items():
        if count < DELTA_COUNT:
            words.count[word] = 1e10  # to decrease the score
    return words


def word_serial(words):
    i = 0
    DELTA_COUNT = 2
    for word, count in words.count.items():
        if count < DELTA_COUNT:
            words.serial[word] = -1
            words.li.append(word)
            i += 1


def phrases_counting(texts, words):
    phrases = dict()
    phrases_count = dict()
    for text in texts:
        for i in range(len(text) - 1):
            if words.count[text[i]] == 1e10 or words.count[text[i + 1]] == 1e10:
                break
            phrases[text[i]] = set()
            phrases[text[i]].add(text[i + 1])
            phrase = (text[i], text[i + 1])
            phrases_count[phrase] = phrases_count.get(phrase, 0) + 1
    return phrases, phrases_count


def score_cal(phrases_count, words):
    score = dict()
    for ((p0, p1), count) in phrases_count.items():
        score[(p0, p1)] = count / words[p0] / words[p1]
    return score


def score_sort(score):
    score_sorted = sorted(score.items(), key=lambda x: x[1], reverse=True)
    return score_sorted


def new_word_sort(word):
    word_sorted = sorted(word.items(), key=lambda x: x[1], reverse=True)
    tmp = list()
    for word, score in word_sorted:
        tmp.append(word)
    new_word_sorted = tuple(tmp)
    return new_word_sorted


def phrase_2_new_word(phrases_count, scores, delta=1e-3):
    new_words = dict()
    word_start = dict()

    def new_word_start_with(_new_word, _word1):
        if _word1 not in word_start:
            word_start[_word1] = list()
        word_start[_word1].append(_new_word)
        return word_start

    for (w1, w2), score in scores.items():
        if score > delta:
            new_word = w1 + w2
            new_words[new_word] = phrases_count[(w1, w2)]
            new_word_start_with(new_word, w1)
    return new_words, word_start


def phrase_merge_in_text(word_start, texts):
    def replace_text(_text, _ind, _word):
        _text.pop(_ind)
        _text.pop(_ind)
        _text.insert(_ind, _word)

    i = 0
    for text in texts:
        i += 1
        # print(i)
        index = -1
        while True:
            index += 1
            if index >= len(text) - 1:
                break
            if text[index] not in word_start:
                continue

            text_word = text[index] + text[index + 1]
            if text_word in word_start[text[index]]:
                pass
                replace_text(text, index, text_word)


def save_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load(filename, data):
    with open(filename, 'rb') as f:
        data = pickle.load(f)


if __name__ == '__main__':
    Filename = 'train.txt'
    LINE_NUM = 4e4
    Data = readfile(Filename, LINE_NUM)
    print('File completed')
    Texts = text_init(Data)
    del Data
    print('Text completed')
    for itr in range(3):
        print(itr)
        Words = words_counting(Texts)
        print('Words completed')
        Phrases, Phrases_count = phrases_counting(Texts, Words)
        print('Phrases completed')
        Score = score_cal(Phrases_count, Words.count)
        del Words
        # Score_sorted = score_sort(Score)
        print('Score completed')
        New_words, Word_start = phrase_2_new_word(Phrases_count, Score, 1e-6)
        # New_words_sorted = new_word_sort(New_words)
        del Score, Phrases_count, Phrases
        print('New_words completed')
        phrase_merge_in_text(Word_start, Texts)
        del Word_start
        print('replace completed')
