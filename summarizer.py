"""Generates an Extractive Summary using TF algorithm."""

import string
from collections import Counter
from heapq import nlargest

import nltk


def gen_word_freq(text):
    stopwords = nltk.corpus.stopwords.words("english")

    keywords = list()
    for token in nltk.word_tokenize(text):
        if not (token in stopwords or token in string.punctuation):
            keywords.append(token)

    return Counter(keywords)


def gen_sentence_scores(text, word_freq):
    sentence_scores = dict()
    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            sentence_scores[sentence] = (
                sentence_scores.get(sentence, 0) + word_freq[word]
            )

    return sentence_scores


def summarize(text, threshold_factor):
    word_frequency = gen_word_freq(text)
    max_frequency = word_frequency.most_common(1)[0][1]

    for word in word_frequency:
        word_frequency[word] /= max_frequency

    sentence_scores = gen_sentence_scores(text, word_frequency)
    threshold = int(len(sentence_scores) * threshold_factor)
    to_select = nlargest(threshold, sentence_scores.values())

    summary = list()
    for sentence, score in sentence_scores.items():
        if score in to_select:
            summary.append(sentence)

    formatted_summary = " ".join(summary)
    return formatted_summary
