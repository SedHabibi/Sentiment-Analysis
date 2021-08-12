# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 20:22:13 2021

@author: Neelabh
"""
import pickle


#Creating a user defined function for classifying the review.
def review_classifier(reviewText):
    file1 = open('review_model.pkl', 'rb')
    file2 = open('features.pkl', 'rb')
    from sklearn.feature_extraction.text import TfidfVectorizer
    #Reloading models.
    classifier_model = pickle.load(file1)
    vocabulary_of_model = pickle.load(file2)
    
    #Transforming user input review to fit in the model.
    new_vectorizer = TfidfVectorizer(decode_error = 'replace', vocabulary = vocabulary_of_model)
    
    vectorized_new_data = new_vectorizer.fit_transform([reviewText])
    processed_data = classifier_model.predict(vectorized_new_data)
    print(processed_data)


reviewText = input('Whats your review = ')
review_classifier(reviewText)
