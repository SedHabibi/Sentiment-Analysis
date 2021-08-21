# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 09:34:54 2021

@author: Neelabh
"""

# Importing the libraries
import pickle
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from matplotlib import pyplot as plt
from dash.dependencies import Input, Output , State
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import wordcloud
from collections import Counter
import numpy as np
from wordcloud import WordCloud, STOPWORDS

#Global variables.
project_name = None
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

#Function that loads the model.
def load_model():
    global scrapped_reviews
    scrapped_reviews = pd.read_csv('scrapped_reviews.csv')
  
    global review_model
    file = open("review_model.pkl", 'rb') 
    review_model = pickle.load(file)

    global vocab
    file = open("features.pkl", 'rb') 
    vocab = pickle.load(file)
    #pie chart
    print('Loading Data......')
    temp = []
    for i in scrapped_reviews['Review']:
        temp.append(check_review(i)[0])
    scrapped_reviews['sentiment'] = temp
    
    positive = len(scrapped_reviews[scrapped_reviews['sentiment']==1])
    negative = len(scrapped_reviews[scrapped_reviews['sentiment']==0])
    
    explode = (0.1,0)  

    langs = ['Positive', 'Negative',]
    students = [positive,negative]
    colors = ['#41fc1c','red']
    plt.pie(students,explode=explode,startangle=90,colors=colors, labels = langs,autopct='%1.2f%%')
    cwd = os.getcwd()
    if 'assets' not in os.listdir(cwd):
        os.makedirs(cwd+'/assets')
    plt.savefig('assets/sentiment.png')
    #wordcloud
    dataset = scrapped_reviews['Review'].to_list()
    str1 = ''
    for i in dataset:
        str1 = str1+i
    str1 = str1.lower()

    stopwords = set(STOPWORDS)
    cloud = WordCloud(width = 800, height = 400,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(str1)
    cloud.to_file("assets/wordCloud.png")
    #drop down
    global chart_dropdown_values
    chart_dropdown_values = {}
    for i in range(400,501):
        chart_dropdown_values[scrapped_reviews['Review'][i]] = scrapped_reviews['Review'][i]
    chart_dropdown_values = [{"label":key, "value":values} for key,values in chart_dropdown_values.items()]
 
#Function that predicts the sentiment of a review.
def check_review(reviewText):
    loaded_vec = TfidfVectorizer(decode_error="replace",vocabulary=vocab)
    vectorised_review = loaded_vec.fit_transform([reviewText])
    return review_model.predict(vectorised_review)

#Function to open a new browser.
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

#UI of the browser.
def create_app_ui():
    main_layout = html.Div(
    [
    html.H1(id='Main_title', children = "Sentiment Analysis with Insights",style={'text-align':'center'}),
    html.Hr(style={'background-color':'black'}),
    html.H2(children = "Pie Chart",style = {'text-align':'center','text-decoration':'underline'}),
    html.P([html.Img(src=app.get_asset_url('sentiment.png'),style={'width':'700px','height':'400px'})],style={'text-align':'center'}),
    html.Hr(style={'background-color':'black'}),
    html.H2(children = "WordCloud",style = {'text-align':'center','text-decoration':'underline'}),
    html.P([html.Img(src=app.get_asset_url('wordCloud.png'),style={'width':'700px','height':'400px'})],style={'text-align':'center'}),
    html.Hr(style={'background-color':'black'}),
    html.H2(children = "Select a Review",style = {'text-align':'center','text-decoration':'underline'}),
    dcc.Dropdown(
                id='Chart_Dropdown', 
                  options=chart_dropdown_values,
                  placeholder = 'Select a Review',style={'font-size':'22px','height':'70px'}
                    ),
    html.H1(children = 'Missing',id='sentiment1',style={'text-align':'center'}),
    html.Hr(style={'background-color':'black'}),
    html.H2(children = "Find Sentiment of Your Review",style = {'text-align':'center','text-decoration':'underline'}),
    dcc.Textarea(
        id = 'textarea_review',
        placeholder = 'Enter the review here.....',
        style = {'width':'100%', 'height':150,'font-size':'22px'}
        ),
    
    dbc.Button(
        children = 'Check Review Sentiment',
        id = 'button_review',
        color = 'dark',
        style= {'width':'100%'}
        ),
    
    html.H1(children = 'Missing', id='result',style={'text-align':'center'})
    
    ]    
    )
    
    return main_layout

#Calling the function.
@app.callback(

    
    Output( 'result'   , 'children'     ),
    [
    Input( 'button_review'    ,  'n_clicks')
    ],
    [
    State( 'textarea_review'  ,   'value'  )
    ]
    )

#Updating the UI as the user clicks.
def update_app_ui_2(n_clicks, textarea_value):

    print("Data Type = ", str(type(n_clicks)))
    print("Value = ", str(n_clicks))


    print("Data Type = ", str(type(textarea_value)))
    print("Value = ", str(textarea_value))


    if (n_clicks > 0):

        response = check_review(textarea_value)
        if (response[0] == 0):
            result = 'Negative'
        elif (response[0] == 1 ):
            result = 'Positive'
        else:
            result = 'Unknown'
        
        return result
        
    else:
        return ""

#Calling the function.
@app.callback(
    Output("sentiment1", "children"),
    [Input("Chart_Dropdown", "value")])

#Showing the sentiment.
def update_sentiment(review1):
    sentiment = []
    if review1:
        if check_review(review1)==0:
            sentiment='Negative' 
        if check_review(review1)==1:
            sentiment='Positive'
    else:
        sentiment='Missing'
    return sentiment


def main():
    print("Start of your project")
    load_model()
    open_browser()

    global scrapped_reviews
    global project_name
    global app
    
    project_name = "Sentiment Analysis with Insights"
    app.title = project_name
    app.layout = create_app_ui()
    app.run_server()
    
    
    
    print("End of my project")
    project_name = None
    scrapped_reviews = None
    app = None
    
        
if __name__ == '__main__':
    main()



