# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:31:37 2021

@author: Neelabh
"""
#Importing necessary libraries.
import pickle
import pandas as pd
from selenium import webdriver
from sklearn.feature_extraction.text import TfidfVectorizer

#Global variables.
date = []
person = []
review_bag = []
review_sentiment = []

#Creating a user defined function for classifying the review.
def review_classifier(reviewText):
    

    file1 = open('review_model.pkl', 'rb')
    file2 = open('features.pkl', 'rb')
    
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
    global date
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
            try:
                print('Clicking on product', i + 1)
                products[i].find_element_by_tag_name('a').click()
            except:
                print('Product doesnt exist.')
            
            #Shifting the focus of webdriver to the new tab.
            windows = browser.window_handles
            browser.switch_to.window(windows[1])
            
            #Scrapping from the etsy site.
            try:
                #xpath for the review panel.
                xpath2 = '//*[@id="same-listing-reviews-panel"]/div'
                product_count = browser.find_element_by_xpath(xpath2)
                product_count = product_count.find_elements_by_class_name('wt-grid__item-xs-12')
                
                for review in range(1, len(product_count) + 1):
                    
                    #Person's name.
                    person_xpath = '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/div[2]/p[1]'
                    person_xpath = review_xpath.format(review)
                    person_data = browser.find_element_by_xpath(person_xpath).text
                    
                    #Conditional statements to make sure tht there are no duplicate entries.
                    if person_data[:person_data.find(',') - 6] not in person:
                        try:
                            #Appendind person's name to the list.
                            person.append(person_data[:person_data.find(',') - 6])
                            
                            #Appending the date to the list.
                            date.append(person_data[person_data.find(',') - 6:])
                            
                        except Exception:
                            person.append('Person not found.')
                            date.append('Date not found.')
                            
                        #Getting the review and it's sentiment as well.
                        try:
                            review_xpath = '//*[@id="review-preview-toggle-{}"]'
                            review_xpath = review_xpath.format(review - 1)
                            product_review = browser.find_element_by_xpath(review_xpath).text
                            
                            #Appending the review.
                            review_bag.append(product_review)
                            
                            #Appending the sentiment.
                            review_sentiment.append(review_classifier(product_review))
                        except Exception:
                            #Error Handling
                            review_bag.append('No reviews for this product.')
                            review_sentiment.append(review_classifier('No reviews for this product.'))

            except Exception:
                try:
                
                    #Alternate xpath for the products table.
                    xpath3 = '//*[@id="reviews"]/div[2]/div[2]'
                    product_count = browser.find_element_by_xpath(xpath3)
                    product_count = product_count.find_elements_by_class_name('wt-grid__item-xs-12')
                    
                    for review2 in range(1, len(product_count) + 1):
                        
                        #Alternate xpath for the person name.
                        person_xpath = '//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/p'
                        person_xpath = person_xpath.format(review2)
                        
                        #Getting the person name.
                        person_data = browser.find_element_by_xpath(person_xpath).text
                        
                        if person_data[:person_data.find(',') - 6] not in person:
                            
                            #Getting unique names and the review's corresponding dates.
                            try:
                                #Appendind person's name to the list.
                                person.append(person_data[:person_data.find(',') - 6])
                                
                                #Appending the date to the list.
                                date.append(person_data[person_data.find(',') - 6:])
                            except:
                                
                                #Handing the error.
                                person.append('Person not found.')
                                date.append('Date not found.')
                            
                            #Getting the review and it's sentiment also.
                            try:
                                review_xpath = '//*[@id="review-preview-toggle-{}"]'
                                review_xpath = review_xpath.format(review2 - 1)
                                product_review = browser.find_element_by_xpath(review_xpath).text
                                
                                #Appending the review.
                                review_bag.append(product_review)
                                
                                #Appending the sentiment.
                                review_sentiment.append(review_classifier(product_review))
                            except Exception:
                                
                                #Error Handling
                                review_bag.append('No reviews for this product.')
                                review_sentiment.append(review_classifier('No reviews for this product.'))
                
                except Exception:
                    try:
                        #Alternate xpath for the products table.
                        xpath4 = '//*[@id="reviews"]/div[2]/div[2]'
                        product_count = browser.find_element_by_xpath(xpath4)
                        product_count = product_count.find_elements_by_class_name('wt-grid__item-xs-12')
                         
                        for review3 in range(1, len(product_count) + 1):
                            
                            #Alternate xpath for person name.
                            person_xpath = '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/p'
                            person_xpath = person_xpath.format(review3)
                            
                            #Getting the name.
                            person_data = browser.find_element_by_xpath(person_xpath).text
                            
                            if person_data[:person_data.find(',') - 6] not in person:
                                #Getting unique names and the review's corresponding dates.
                                try:
                                    #Appendind person's name to the list.
                                    person.append(person_data[:person_data.find(',') - 6])
                                
                                    #Appending the date to the list.
                                    date.append(person_data[person_data.find(',') - 6:])
                                except:
                                    #Handing the error.
                                    person.append('Person not found.')
                                    date.append('Date not found.')
                                
                                #Getting the review and it's sentiment also.
                                try:
                                    review_xpath = '//*[@id="review-preview-toggle-{}"]'
                                    review_xpath = review_xpath.format(review3 - 1)
                                    product_review = browser.find_element_by_xpath(review_xpath).text
                                
                                    #Appending the review.
                                    review_bag.append(product_review)
                                
                                    #Appending the sentiment.
                                    review_sentiment.append(review_classifier(product_review))
                                    
                                except Exception:
                                    #Error Handling
                                    review_bag.append('No reviews for this product.')
                                    review_sentiment.append(review_classifier('No reviews for this product.'))
                                
                    except Exception:
                        print('No records found.')
                        continue
        
            #Closing the tab.
            browser.close()
            
            #Changing the focus to the main tab.
            browser.switch_to.window(windows[0])
    
    except Exception:
        print('Terminating the process.')
    
    browser.quit()
            
                            
#Function to write the data into a csv file.
def data_frame():
    global date
    global person
    global review_bag
    global review_sentiment
    
    #Making the data frame.
    df = pd.DataFrame()
    df['Name'] = person
    df['Review'] = review_bag
    df['Sentiment'] = review_sentiment
    
    #Exporting the data frame into a csv file.
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
 

                              
