# def phrases_counting(data, phrases, k):
#     phrases_count = dict()
#     # phrases length = 724224
#     for d in data:
#         # print(d.id)
#         d = d.case
#         if len(d) <= 1:
#             pass
#         for i in range(len(d) - k):
#             phrases[d[i]].add(d[i + 1])
#             phrase = (d[i], d[i + 1])
#             phrases_count[phrase] = phrases_count.get(phrase, 0) + 1
#     return phrases, phrases_count

def phrase_merge_in_text(new_word, texts):
    def word_exist(_text, _index, _word):
        for i in range(len(_word)):
            if _text[index + i] != _word[i]:
                return False
        return True

    def replace_text(_text, _ind, _word):
        for i in range(len(_word)):
            _text.pop(_ind)
        _text.insert(_ind, _word)

    i = 0
    for text in texts:
        print(i)
        i += 1
        for word in new_word:
            index = 0
            for letter_t in text:
                if letter_t[0] == word[0] and len(text) >= index + len(word):
                    if word_exist(text, index, list(word)):
                        replace_text(text, index, word)
                index += 1