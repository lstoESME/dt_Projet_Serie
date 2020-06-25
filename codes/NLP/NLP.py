# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:40:27 2020

@author: stosc
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
import nltk
import string
from string import digits
nltk.download('stopwords')
import re

# Load stop words from nltk.
nltk_stopwords = set(nltk.corpus.stopwords.words("english")) 

# Load stop words from sklearn.
sklearn_stopwords = set(ENGLISH_STOP_WORDS)

# Load list of non-significative words.
useless = open("C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\Datatools\\Projet\\useless_word.txt", "r")
useless_words = useless.readlines()
for n in range(len(useless_words)):
    useless_words[n] = useless_words[n].rstrip('\n')
    
# Union on all 3 lists "stop_words".
STOP_WORDS = nltk_stopwords.union(sklearn_stopwords).union(useless_words)


# Load data that contains series storylines.
df_storylines = pd.read_csv("C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\series_storylines.csv",
                      header=0, index_col=0)
#type(df_storylines)

# Create dataframe with top 10 series.
df_top_ten = pd.DataFrame(df_storylines.iloc[0:10,0])


"""Clean Data"""

# Convert all text to lowercase.
df_storylines["Storyline"] = df_storylines["Storyline"].str.lower()


def remove_punctuation(story):
    
    """
    
    Remove the puncutation on a word. For exemple "good." : remove the dot from good.
    
    :param story: the dataframe that contains the storyline text.
    :type story: pandas dataframe.
    :return: storyline without the punctuation on the words.
    :rtype: string.
    
    """
    rem_punct = str.maketrans("","", string.punctuation)
    result = story.translate(rem_punct)
    
    return result


def remove_digits(story):
    
    """
    
    Remove the puncutation on a word. For exemple "good." : remove the dot from good.
    
    :param story: the dataframe that contains the storyline text.
    :type story: pandas dataframe.
    :return: each storyline without digits.
    :rtype: string.
    
    """
    
    remove_digits = str.maketrans("", "", digits)
    result = story.translate(remove_digits)
    
    return result

df_storylines["Storyline"] = df_storylines["Storyline"].apply(remove_punctuation)
df_storylines["Storyline"] = df_storylines["Storyline"].apply(remove_digits)


"""Analyse Data : countVectorizer"""

cv = CountVectorizer(stop_words = STOP_WORDS, ngram_range=(1,1), max_features=2000)

# Apply CV on train data
cv.fit(df_storylines["Storyline"])
cv_transform = cv.transform(df_storylines["Storyline"])
new_df_storylines = pd.DataFrame(cv_transform.toarray(), columns=cv.get_feature_names())

word_frequency = new_df_storylines.sum(axis=0).sort_values(ascending=False)

plt.figure(figsize=(30, 60))
word_frequency[:100].plot.barh()
plt.title("Distribution of Word frequency (Top 100)")
plt.xlabel("Words")
plt.ylabel("Frequency")
#plt.show()


"""Analyse Data : TF-IDF"""

from  sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(lowercase=True, 
                         stop_words=STOP_WORDS, 
                         ngram_range=(1,1), 
                         max_features=2000)
# Transform list of documents to matrice : fréquency
csr_mat = tfidf.fit_transform(df_top_ten["Storyline"])
#csr_mat.toarray()
words = tfidf.get_feature_names()
df_tfidf = pd.DataFrame(index=df_top_ten["Storyline"], data=csr_mat.toarray(), columns=words)

#Print usefull words : not high frequency, bring a difference
inverse_document_freq = pd.DataFrame({"idf":tfidf.idf_}, 
                                     index=tfidf.get_feature_names())
inverse_document_freq = inverse_document_freq.sort_values(by="idf", ascending=False)

plt.figure(figsize=(16, 8))
plt.title("Distribution of Inverse document frequency (Top 50)")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.bar(height=inverse_document_freq[:50]['idf'], 
        x=inverse_document_freq[:50].index)
plt.xticks(rotation=90)
plt.show()















