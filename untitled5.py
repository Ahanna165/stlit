# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TlHWJ1uLY3go2W1yH8Nf-Eynu2BrV2EB
"""

#!pip install streamlit
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
print(nltk.__version__)

from collections import Counter

# Load CSV data
@st.cache
def load_data():
    return pd.read_csv('/content/un-general-debates.csv')

table = load_data()

# Basic data processing
table['length'] = table['text'].str.len()
table['AVG'] = table.groupby('year')['length'].transform('mean').round()

# Set Streamlit app title
st.title("UN Assembly Speeches Comparison")

# Sidebar filters
st.sidebar.header("Filters")
countries = table['country'].unique()
selected_countries = st.sidebar.multiselect('Select two countries for comparison', countries, default=['UKR', 'RUS'])

min_year = int(table['year'].min())
max_year = int(table['year'].max())
selected_years = st.sidebar.slider('Select the year range', min_year, max_year, (min_year, max_year))

# Filter by selected countries and year range
filtered_data = table[(table['country'].isin(selected_countries)) &
                      (table['year'] >= selected_years[0]) &
                      (table['year'] <= selected_years[1])]

# Function to clean and tokenize text
nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('english'))
stopwords.update({'united', 'nations'})

def clean_text(text):
    tokens = text.lower().split()  # Basic tokenization
    tokens = [t for t in tokens if t not in stopwords]  # Remove stopwords
    return tokens

# Apply cleaning to text
filtered_data['cleaned_text'] = filtered_data['text'].apply(clean_text)

# Generate WordClouds
def generate_wordcloud(text):
    wordcloud = WordCloud(max_words=100, stopwords=stopwords, background_color='white').generate(' '.join(text))
    return wordcloud

country1_data = filtered_data[filtered_data['country'] == selected_countries[0]]['cleaned_text'].sum()
country2_data = filtered_data[filtered_data['country'] == selected_countries[1]]['cleaned_text'].sum()

if country1_data and country2_data:
    # Generate word clouds
    wc_country1 = generate_wordcloud(country1_data)
    wc_country2 = generate_wordcloud(country2_data)

    # Display word clouds
    st.subheader(f"Word Cloud for {selected_countries[0]}")
    fig1, ax1 = plt.subplots()
    ax1.imshow(wc_country1, interpolation='bilinear')
    ax1.axis('off')
    st.pyplot(fig1)

    st.subheader(f"Word Cloud for {selected_countries[1]}")
    fig2, ax2 = plt.subplots()
    ax2.imshow(wc_country2, interpolation='bilinear')
    ax2.axis('off')
    st.pyplot(fig2)
else:
    st.write("No data available for the selected countries and years.")

# Show statistics like speech lengths
st.write(f"Average Speech Length for {selected_countries[0]}: {filtered_data[filtered_data['country'] == selected_countries[0]]['length'].mean()}")
st.write(f"Average Speech Length for {selected_countries[1]}: {filtered_data[filtered_data['country'] == selected_countries[1]]['length'].mean()}")

