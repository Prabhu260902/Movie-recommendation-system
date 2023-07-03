import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



css = """
<style>
    
    .img{
        height:300px;
        width: 220px;
        transition: transform 0.5s;
    }
    .p1{
    color: blue;
        transition: transform 0.5s;
    }

    .p1:hover{
        color: red;
        transform: scale(1.5);
    }
    .img:hover {

        transform: scale(0.9);
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def movie_title(movie_name):
    movie_name = movie_name.lower()
    a = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in movie_name:
        if i not in a:
            if(i==" " or i=="." or i=="-" or i==','):
                movie_name  =movie_name.replace(i,'-')
            else:
                movie_name = movie_name.replace(i, '')
    if(movie_name[-1] not in a):
        movie_name  = movie_name[:-1]

    return movie_name


def recommend(movie):
  index = movies[movies['title'] == movie].index[0]
  movie_list = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[0:15]
  l=[]
  k=[]


  for i in movie_list:
      movie_id = movies.iloc[i[0]].movie_id
      l.append(movies.iloc[i[0]].title)
      k.append(fetch_poster(movie_id))

  return l,k

movies_dict = pickle.load(open('movies_dict.pkl','rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie recommender system')

selected_movie_name = st.selectbox('Select a movie',movies['title'].values)





def show(movie_id,movie_name):

    st.markdown('''
            <a href="https://www.youtube.com/results?search_query= ''' + movie_name + '''" style="color: red,border:2px solid red">
                 <img class="img" src= ''' + movie_id + ''' style="color: red,border:2px solid red" width='220' height='300' />''',
        unsafe_allow_html=True
        )
    st.markdown('''
                <center><h5>'''+movie_name+'''</h5></center> ''',
                unsafe_allow_html=True
                )



    movie_name = movie_title(movie_name)
    st.markdown('''
                <a href= "https://www.justwatch.com/in/movie/''' +movie_name+ ''' " style="color:black">
                     <center><b><p class="p1"> StreamingON </p></b></center> ''',
                unsafe_allow_html=True
                )

    st.write("---------------------------------------------")




if st.button('Recommend'):
    st.markdown('''
            <marquee behavior="alternate" Scrollamount=10 onmouseover="this.stop()" onmouseout="this.start()"><h5> Click on image to watch trailer </h5></marquee> ''',
            unsafe_allow_html=True
    )
    names, posters = recommend(selected_movie_name)
    col1, col2, col3 ,col4 ,col5= st.columns(5)

    for i in range(15):
        if(i<3):
            with col1:
                show(posters[i],names[i])

        elif (i < 6):
            with col2:
                show(posters[i], names[i])

        elif (i < 9):
            with col3:
                show(posters[i], names[i])

        elif (i < 12):
            with col4:
                show(posters[i], names[i])

        else:
            with col5:
                show(posters[i], names[i])










