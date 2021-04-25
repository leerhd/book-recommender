import streamlit as st
import recommender
import dashboard


def main():
    st.set_page_config(
        page_title='Book Warehouse',
        page_icon='📚',
        layout='centered',
        initial_sidebar_state='auto',
    )

    st.sidebar.title('📚 Book Warehouse')
    st.sidebar.header('')

    pages = {'Recommender': recommender, 'Dashboard': dashboard}

    menu_select = st.sidebar.radio('', list(pages.keys()))
    page = pages[menu_select]
    page.app()


if __name__ == '__main__':
    main()
