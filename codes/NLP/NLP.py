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
STOP_WORDS = nltk_stopwords.union(sklearn_stopwords)
#STOP_WORDS = nltk_stopwords.union(sklearn_stopwords).union(useless_words)

#print(STOP_WORDS)

# Load data that contains series storylines.
df_storylines = pd.read_csv("C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\series_storylines.csv",
                      header=0, index_col=0)

type(df_storylines)


# Convert all text to lowercase.
df_storylines["Storyline"] = df_storylines["Storyline"].str.lower()

liste=[]
for n in range(len(df_storylines)):
    
    words_storyline = df_storylines.iloc[n, 0].split() # Chaque mot de la liste
    
    # Remove punctuation from a string.
    remove_punctuation = str.maketrans("","", string.punctuation)
    for n in range(len(words_storyline)):
        words_storyline[n] = words_storyline[n].translate(remove_punctuation)
        liste.append(words_storyline)
type(liste)

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


cv = CountVectorizer(stop_words = STOP_WORDS, ngram_range=(1,1), max_features=500)

Xtrain, x_test, y_train, y_test = train_test_split(df_storylines, test_size=0.2)
df_storyline_train.shape()

# Apply CV on train data

cv.fit(df_storylines["Storyline"])

train_cv = cv.transform(df_storylines_train["Storyline"])
test_cv = cv.transform(df_storylines_test["Storyline"])

new_df_storylines = pd.DataFrame(train_cv.toarray(), columns=cv.get_feature_names())

new_df_storylines = new_df_storylines.drop('series', axis=1)
new_df_storylines.head(1)

word_frequency = new_df_storylines.sum(axis=0).sort_values(ascending=False)
word_frequency

plt.figure(figsize=(30, 60))
word_frequency[:300].plot.barh()
plt.title("Distribution of Word frequency (Top 300)")
plt.xlabel("Words")
plt.ylabel("Frequency")
#plt.show()























