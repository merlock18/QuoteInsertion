import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

st.title('Quotes to Scrape')

tag = st.selectbox('Select a topic for quotes', ['love', 'inspirational', 'life', 'humor', 'books', 'reading', 'friendship', 'friends', 'truth', 'simile'])

generate = st.button('Generate Quotes')

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
    st.code(text)
    st.write(author)
    st.code(path)
    st.markdown(f'<a href="http://quotes.toscrape.com{path}">{author}</a>', unsafe_allow_html=True)
    quote_file.append([text, author, path])

if generate:
    try:
        df = pd.DataFrame(quote_file)
        st.dataframe(df)
        df.to_csv(f'quotes_{tag}.csv', index=False, header=['Quote', 'Author', 'URL'], encoding='utf-8')
    except:
        st.write('No quotes found')
    