import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from supabase import create_client, Client

st.sidebar.title('Quotes to Scrape')

tag = st.sidebar.selectbox('Select a topic for quotes', ['love', 'inspirational', 'life', 'humor', 'books', 'reading', 'friendship', 'friends', 'truth', 'simile'])

insert = st.sidebar.button('Insert Quotes')

url = f'http://quotes.toscrape.com/tag/{tag}/'

# st.write(f'Quotes about {url}')

response = requests.get(url)

# st.write(response)

content = BeautifulSoup(response.content, 'html.parser')

quotes = content.find_all('div', class_='quote')

# st.write(quotes)

quote_file = []

for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    path = quote.find('a')['href']
    st.success(text)
    st.markdown(f'<a href="http://quotes.toscrape.com{path}">{author}</a>', unsafe_allow_html=True)
    quote_file.append([text, author, path])



if insert: 
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        supabase = create_client(url, key)
        bulk_insert = []
        for row in quote_file:
            # st.write(f"{row[0]} :{row[1]}: {row[2]}")
            bulk_insert.append({ "quote": row[0],"author": row[1], "url": row[2]})
            # st.write(bulk_insert)
        st.code(bulk_insert)
        result = supabase.table("Quote").insert(bulk_insert).execute()
        st.write(f'Rows inserted!')
    except:
        st.error('Error: No rows inserted')
    