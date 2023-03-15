import wikipedia, nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def get_wiki_words(article, filter):
    '''
    Takes in a wikipedia article name and a boolean "filter" which decides if stopwords
    should be removed from the article content. Returns a list of strings where each string
    is a word from the article.
    ---------------------------------------------------------------------------------------
    inputs: article (string), filter (bool)
    returns: tokenized text (list of strings)
    '''
    text = wikipedia.page(str(article)).content
    
    if filter:
        words = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        filtered_words = []
        for word in words:
            if word.casefold() not in stop_words:
                filtered_words.append(word)
        return filtered_words
    else:
        return word_tokenize(text)

def get_wiki_sentences(article):
    '''
    Takes in a wikipedia article name and returns the content of the article as a list of 
    strings where each string is a sentence.
    -------------------------------------------------------------------------------------
    inputs: article (string)
    returns tokenized text (list of strings)
    '''
    text = wikipedia.page(str(article)).content
    return sent_tokenize(text)
