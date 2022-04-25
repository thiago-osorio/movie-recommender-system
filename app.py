import pickle
import requests
import streamlit as st 
import pandas as pd

def get_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c752658cbea631866744f576a4013cd1'.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
    return full_path

def sistema_recomendacao(movie):
    index = filmes.loc[filmes['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x:x[1])
    
    filmes_recomendados_nomes = []
    filmes_recomendados_poster = []
    
    for i in distance[1:5]:
        movie_id = filmes.iloc[i[0]].id
        filmes_recomendados_poster.append(get_poster(movie_id))
        filmes_recomendados_nomes.append(filmes.iloc[i[0]].title)
        
    return filmes_recomendados_nomes, filmes_recomendados_poster


st.header('Sistema de Recomendação de Filmes')
dict_filmes = pickle.load(open('Modelos/lista_filmes.pkl', 'rb'))
similarity = pickle.load(open('Modelos/similarity.pkl', 'rb'))
filmes = pd.DataFrame(dict_filmes)


movie_list = filmes['title'].values
select_movies = st.selectbox('Selecione o Filme', movie_list)

if st.button('Mostrar Recomendações'):
    filmes_recomendados_nomes, filmes_recomendados_poster = sistema_recomendacao(select_movies)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(filmes_recomendados_nomes[0])
        st.image(filmes_recomendados_poster[0])
    with col2:
        st.text(filmes_recomendados_nomes[1])
        st.image(filmes_recomendados_poster[1])
    with col3:
        st.text(filmes_recomendados_nomes[2])
        st.image(filmes_recomendados_poster[2])