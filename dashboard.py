import recommender
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go


def app():
    st.image('img/top.png')
    st.title('Dashboard')
    st.markdown('_(Internal Business Use)_')

    books, chart, _, _, _ = recommender.load_data()

    st.header('')
    st.text('')
    st.header('📊 Visualizations')
    st.text('')
    selected = st.selectbox('', ['Book Ratings', 'Top Books', 'Publication Year', 'Correlation Matrix'])
    st.text('')

    if selected == 'Book Ratings':
        fig = px.pie(chart,
                     names='rating',
                     values='count',
                     labels={'rating': 'Book Rating'},
                     template='plotly_dark')
        fig.update_layout(title_text='Overall Book Ratings',
                          title_x=0.5)
        fig.update_traces(textposition='inside',
                          textinfo='percent+label')
        st.plotly_chart(fig)

        fig = px.box(books[['average_rating']],
                     x='average_rating',
                     labels={'average_rating': 'Average Book Rating'},
                     template='plotly_dark')
        fig.update_layout(title_text='Average Book Ratings',
                          title_x=0.5)
        st.plotly_chart(fig)

    elif selected == 'Top Books':
        fig = px.bar(books.nlargest(10, 'ratings_count').sort_values('ratings_count', ascending=False),
                     x='ratings_count',
                     y='title',
                     labels={'ratings_count': 'Number of Ratings', 'title': ''},
                     orientation='h',
                     color='title')
        fig.update_layout(title_text='Most Popular Books',
                          title_x=0.5,
                          margin=dict(l=375),
                          showlegend=False)
        fig.update_yaxes(automargin=False)
        st.plotly_chart(fig)

        fig = px.bar(books.nlargest(10, 'average_rating').sort_values('average_rating', ascending=False),
                     x='average_rating',
                     y='title',
                     labels={'average_rating': 'Average Rating', 'title': ''},
                     orientation='h',
                     color='title')
        fig.update_layout(title_text='Top Rated Books',
                          title_x=0.5,
                          margin=dict(l=375),
                          showlegend=False)
        fig.update_yaxes(automargin=False)
        st.plotly_chart(fig)

    elif selected == 'Publication Year':
        fig = px.histogram(books[['original_publication_year']],
                           x='original_publication_year',
                           range_x=[1900, 2017],
                           nbins=5000,
                           labels={'original_publication_year': 'Publication Year'},
                           template='plotly_dark')
        fig.update_layout(title_text='Publication Years',
                          yaxis_title_text='Number of Books',
                          title_x=0.5)
        st.plotly_chart(fig)

    elif selected == 'Correlation Matrix':
        corr = books[['books_count', 'original_publication_year', 'average_rating', 'ratings_count',
                      'work_ratings_count', 'work_text_reviews_count']].corr()
        fig = go.Figure(go.Heatmap(z=corr.values, x=corr.index.values, y=corr.columns.values))
        fig.update_layout(title={'text': 'Correlation Matrix Heatmap', 'x': 0.5, 'xanchor': 'center'})
        st.plotly_chart(fig)

    st.header('')
    st.text('')
    st.header('📁 Data Sample')
    st.text('')
    st.write(books.head(100))
    st.write('Data obtained from https://github.com/zygmuntz/goodbooks-10k')
