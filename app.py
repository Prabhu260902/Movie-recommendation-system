import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
  index = movies[movies['title'] == movie].index[0]
  movie_list = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[0:10]
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


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    st.image(posters,width=130,caption=names)
