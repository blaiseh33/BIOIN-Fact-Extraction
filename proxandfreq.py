import wikiscrape
punctuation = {'.', ',', ';', '-', '/', '?', '!', '%', '(', ')', '==', '='}
max_proximity = 40
filter_stopwords = True


def get_word_frequencies(article):
    '''
    Takes in a wikipedia article name as an argument and returns a dictionary of each word
    and their corresponding frequency (# of occurrences) in the article.
    --------------------------------------------------------------------------------------
    inputs: article (string)
    returns: sorted_word_freq (dict)
    '''
    raw_words = wikiscrape.get_wiki_words(article, filter_stopwords)
    words = []

    # remove punctuation
    for word in raw_words:
        if word.casefold() not in punctuation:
            words.append(word)

    word_freq = dict.fromkeys(words, 0)

    # count frequency of each word
    for word in words:
        word_freq[word] += 1

    sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x:x[1], reverse=True))
    return sorted_word_freq


def get_word_proximities(article, keyword):
    '''
    Takes in a wikipedia article name and chemical word to find the proximity of all words
    to this chemical keyword. Returns a dictionary of each word and a list of their
    distances to the keyword as the dictionary value
    --------------------------------------------------------------------------------------
    inputs: article (string), keyword (string)
    returns: word_prox (dict)
    '''
    raw_words = wikiscrape.get_wiki_words(article, filter_stopwords)
    words = []

    # remove punctuation
    for word in raw_words:
        if word.casefold() not in punctuation:
            words.append(word)

    word_prox = dict.fromkeys(words, [])

    # get indexes of keyword in text
    keyword_indices = []
    for i in range(len(words)):
        if words[i].casefold() == keyword.casefold():
            keyword_indices.append(i)

    # find proximity of <keyword> to each word in text, with a limit of <max_proximity>
    for i in range(len(words)):
        distances = closest_keywords(keyword_indices, i)
        #print("Distances for " + words[i] + ": " + str(distances))
        word_prox[words[i]] = distances

    return word_prox


def closest_keywords(keyword_indices, index):
    '''
    Takes in the location (indices) of a keyword and a specific index of another word
    and returns the distances of the word from the keyword locations as a list
    ---------------------------------------------------------------------------------
    inputs: keyword_indeces (list of ints), index (int)
    returns: distances (list of ints)
    '''
    distances = []
    for i in range(len(keyword_indices)):
        dist = abs(keyword_indices[i] - index)
        if dist <= max_proximity:
            distances.append(dist)
    return distances