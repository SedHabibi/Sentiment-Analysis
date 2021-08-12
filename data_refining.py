# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 14:46:55 2021

@author: Neelabh
"""
#Importing libraries.
import re
import nltk
import pickle
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.metrics import roc_auc_score
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

#Basic data management.
data = pd.read_csv("balanced_reviews.csv")
data.dropna(inplace = True)
data = data[data['overall'] != 3]

#Data cleaning.
review_bag = []
nltk.download('stopwords')
for i in range(len(data)):
    review = re.sub('[^a-zA-Z]', ' ', data.iloc[i,1])
    review = review.lower()
    
    #Removing extra whitespaces.
    review = review.split()
    
    #Removing stopwords.
    review = [word for word in review if not word in stopwords.words('english')]
    
    #Stemming.
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review]
    review = ' '.join(review)
    
    #Adding the review in a list.
    review_bag.append(review)

data['positivity'] = np.where(data['overall'] > 3, 1, 0)

'''
Now features is the review_bag and labels will be the positivity column in the dataframe. 
'''
features = review_bag
labels = data['positivity'].values 

#Splitting data into test and train subsets.
features_train, features_test, labels_train, labels_test = tts(features, labels, train_size = 0.75, random_state = 42)

#Vectorizing data and fitting it.
vect = TfidfVectorizer(min_df = 5).fit(features_train)
new_features = vect.transform(features_train)

#Model building.
model = LogisticRegression()
model.fit(new_features, labels_train)
predictions = model.predict(vect.transform(features_test))

#Getting model score and confusion matrix.
confusion_matrix(labels_test, predictions)

roc_auc_score(labels_test, predictions)

'''
Getting a model score of 88.06% and confusion matrix of ->
[[58197,  7576],
 [ 8159, 57914]]
'''
model_file = open('review_model.pkl', 'wb')
pickle.dump(model, model_file)

vocabulary_file = open('features.pkl', 'wb')
pickle.dump(vect.vocabulary_, vocabulary_file)

model_file.close()
vocabulary_file.close()





