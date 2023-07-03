import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


movies_data = pd.read_csv('/content/movies.csv')

selected_features = ['genres','keywords','tagline','cast','director']

for col in selected_features:
  movies_data[col] = movies_data[col].fillna('')

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

similarites = cosine_similarity(feature_vectors)


search_movie = input('Enter movie name: ')

movie_names = movies_data['title'].tolist()

corrected_movie_name = difflib.get_close_matches(search_movie,movie_names)
close_movie = corrected_movie_name[0]

index_of_movie = movies_data[movies_data.title == close_movie]['index'].values[0]

similarity_score = list(enumerate(similarites[index_of_movie]))

sorted_movies = sorted(similarity_score,key = lambda x:x[1], reverse=True)

print('Movies suggested for you :')
i=1
for movie in sorted_movies:
  index=movie[0]
  title_from_index=movies_data[movies_data.index==index]['title'].values[0]
  if(i<=30):
    print(i,'. ',title_from_index)
    i+=1