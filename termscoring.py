import proxandfreq as paf


# testing
def main():
    article_name = input("Enter the name of a Wikipedia article: ")
    keyword = input("Enter the name of the chemical to study: ")
    word_scores = get_word_scores(article_name, keyword)
    print("Word Scores:")
    for key, val in word_scores.items():
        print("{0}: {1:.3f}".format(key, val))


def get_word_scores(article, keyword):
    '''
    Takes in a wikipedia article name and chemical keyword and returns a dict of each word 
    and that word's score of relevance using frequency and proximity
    --------------------------------------------------------------------------------------
    inputs: article (string), keyword (string)
    returns: word_scores (dict)
    '''
    words_freq = paf.get_word_frequencies(article)
    words_prox = paf.get_word_proximities(article, keyword)
    word_scores = {}

    # create scores dictionary
    for key, val in words_freq.items():
        word_scores[key] = 1
    for word, score in word_scores.items(): # loop over each word in the dictionary
        prox_score = 1
        for i in range(len(words_prox[word])): # size of list of proximities for each word
            prox_score += 100 / (words_prox[word][i] +1)
        word_scores[word] *= words_freq[word] + prox_score
    
    return word_scores

main()