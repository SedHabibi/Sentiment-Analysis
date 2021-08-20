# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:31:37 2021

@author: Neelabh
"""
#Importing necessary libraries.
import pickle
import time as t
import pandas as pd
from selenium import webdriver
from sklearn.feature_extraction.text import TfidfVectorizer

#Global variables.
person = []
review_bag = []
review_sentiment = []

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
    return processed_data[0]
#Function to scrap data from the etsy site.
def data_scrapper(page):
    global person
    global review_bag
    global review_sentiment
    print('Initiating chrome!')
    browser = webdriver.Chrome(executable_path = 'D:\Python\Python Codes\chromedriver.exe')
    
    url = 'https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page={}'
    
    
    try:
        url = url.format(page)
        browser.get(url)
        
        print('Getting data from page', page)
        
        #xpath for the product table.
        xpath1 = '/html/body/div[5]/div/div[1]/div/div[5]/div[2]/div[2]/div[4]/div/div/div/ul'
        
        #Total number of products on the table.
        products = browser.find_element_by_xpath(xpath1)
        products = products.find_elements_by_tag_name('li')
        
        #Clicking on each product.
        for i in range(len(products)):
            t.sleep(3)
            try:
                print('Clicking on product', i + 1)
                products[i].find_element_by_tag_name('a').click()
            except:
                print('Product doesnt exist.')
            
            #Shifting the focus of webdriver to the new tab.
            windows = browser.window_handles
            browser.switch_to.window(windows[1])
            
            #Getting person name and review from the product.
            try:
                print('Getting the reviews from this product!')
                #id for the review panel.
                id1 = 'same-listing-reviews-panel'
                
                #Getting number of reviews.
                no_of_review = browser.find_element_by_id(id1)
                no_of_review = len(no_of_review.find_elements_by_class_name('wt-grid__item-xs-12 '))
                
                #xpath for person name.
                xpath2 = '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/div[2]/p[1]'
                
                #ID for the review by the person.
                review_id = "review-preview-toggle-{}"
                
                for review in range(1, no_of_review + 1):
                    xpath2 = xpath2.format(review)
                    
                    person_name = browser.find_element_by_xpath(xpath2).text
                    
                    #Appending the name to a list and also making sure that there are no duplicates.
                    
                    if person_name[:person_name.find(',') - 6] not in person:
                        try:
                            person.append(person_name[:person_name.find(',') - 6])
                        except Exception:
                            print('Person doesnt exist.')
                    
                    #Getting review.
                    try:
                        review_id = review_id.format(review - 1)
                        
                        review_data = browser.find_element_by_id(review_id).text
                        
                        #Appending the review in the review list and it's sentiment in the review_sentiment list.
                        if review_data not in review_bag:
                            try:
                                review_bag.append(review_data)
                                sentiment__ = review_classifier(review_data)
                                review_sentiment.append(sentiment__)
                                
                            except:
                                print('No review for this product.')
                    
                    except:
                        print('No review.')
                
            
            except:
                print('\nProduct does not exist!')
            
    
            
            browser.close()
            browser.switch_to_window(windows[0])
        
    except:
        print('Page doesnt exist!')
    
    print('\n')
    if page == 250:
        print('Closing Chrome!!')
        browser.quit()
    
#Function to write the data into a csv file.
def data_frame():
    df = pd.DataFrame()
    df['Name'] = person
    df['Review'] = review_bag
    df['Sentiment'] = review_sentiment
    
    df.to_csv('scrapped_reviews.csv', index = False)
    
#Main function.
def main():
    #Iterating through various pages.
    for page_no in range(1, 251):
        data_scrapper(page_no)
    
    #Getting the csv file.
    data_frame()
    print('Task finished!!')
    
#Calling the main function.
if __name__ == '__main__':
    main()
 

                              