import os
import streamlit as st
import pandas as pd
from surprise import dump
from PIL import Image
from urllib.request import urlopen, urlretrieve


@st.cache(allow_output_mutation=True, persist=True)
def load_data():
    books = pd.read_csv('data/books.csv')
    chart = pd.read_csv('data/chart.csv')

    book_list = sorted(books['title'].tolist())
    book_list.insert(0, '')

    title_to_id = books.set_index('title').to_dict()['book_id']
    id_to_title = books[['book_id', 'best_book_id', 'title', 'authors', 'image_url']].set_index(
        'book_id').T.to_dict('list')

    return books, chart, book_list, title_to_id, id_to_title


@st.cache(allow_output_mutation=True, persist=True)
def download_model():
    url = 'https://github.com/leerhd/book-recommender/releases/download/v1.0/item_model'
    filename = url.split('/')[-1]
    urlretrieve(url, filename)
    item_model = dump.load(filename)[1]
    os.remove(filename)
    return item_model


def display_books(book_recs, index):
    best_book_id = book_recs[index][0]
    book_title = book_recs[index][1]
    book_author = book_recs[index][2].split(',')[0]
    book_cover = book_recs[index][3]

    image = Image.open(urlopen(book_cover))
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image_resized = image.resize((120, 180))
    st.image(image_resized, caption=book_author, width=120)
    link = 'https://www.goodreads.com/book/show/' + str(best_book_id)
    hyperlink = '[' + book_title + '](' + link + ')'
    st.write(hyperlink)


def app():
    st.image('img/top.png')
    st.title('Welcome to Book Warehouse')
    st.header('')
    st.header('')

    _, _, book_list, title_to_id, id_to_title = load_data()
    item_model = download_model()

    selected = st.selectbox('Book Recommender:', book_list,
                            help='This generates a list of book recommendations based on your chosen book.')

    if selected != '':
        book_id = title_to_id[selected]
        book_inner_id = item_model.trainset.to_inner_iid(book_id)

        book_recs = item_model.get_neighbors(book_inner_id, k=8)
        book_recs = (item_model.trainset.to_raw_iid(inner_id) for inner_id in book_recs)
        book_recs = [id_to_title[book_id] for book_id in book_recs]

        st.spinner()
        with st.spinner(text='Finding book recommendations...'):
            st.header('')
            st.header('')
            st.subheader('Books you may also be interested in:')

            st.subheader('')
            first_row = st.beta_columns(4)

            st.header('')
            second_row = st.beta_columns(4)

            for index, item in enumerate(first_row):
                with item:
                    display_books(book_recs, index)

            for index, item in enumerate(second_row):
                with item:
                    index = index + 4
                    display_books(book_recs, index)
    else:
        st.info('Please type a book title into the search bar or select one from the dropdown.')
