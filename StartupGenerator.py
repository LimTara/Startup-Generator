import cohere 
import streamlit as st 
import os 
import textwrap 
import json

# Set up Cohere client 
co = cohere.ClientV2("INSERT API KEY HERE") # Get your free API key: https://dashboard.cohere.com/api-keys 


def generate_unique_movies(genre, temperature, existing_movies):
    
    while True:
        movie_recommendation = generate_movies(genre, temperature)
        if movie_recommendation not in existing_movies:
            existing_movies.append(movie_recommendation)
            return movie_recommendation

def generate_movies(genre, temperature):
    
    prompt = f"""
Generate one movie given the genre of interest by the user. The movie you recommend must be a real world movie and without additional commetary.
Furthermore, the movie you recommend must suit the age group based on user's input. For example, if user's input for age was 10, you should recommend movies suitable for children like cartoons or disney movies.
The things below are examples of what movies you should recommend based on user's input of genre:

Genre: Action
Movie Recommendation: Star Wars, Marvel, Indiana Jones, Black Panther, etc

Genre: Fantasy
Movie Recommendation: The Chronicals of Narnia, Harry Potter, Fantastic Beasts, The Lord of the Rings, Spirited Away, etc

Genre: Horror
Movie Recommendation: Dark Water, The Exorcist, Psycho, Midsommar, etc

Genre: Documentary
Movie Recommendation: Blackfish, Free Solo, Fly, The Founder, etc

Genre: {genre}
Movie Recommendation:"""

    # Call the Cohere Chat endpoint
    response = co.chat( 
            messages=[{"role": "user", "content": prompt}],
            model="command-r-plus-08-2024")
        
    return response.message.content[0].text


def generate_description(movie, temperature):
    
    prompt= f"""
After providing a movie recommendation, you must also provide a description about the movie using 2-3 sentences. For example, if you suggested the movie Spirited Away, 
you would write 'During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches and spirits, and where humans are changed into beasts.'
Below are a list of other examples for movie descriptions:

Movie Name: Star Wars
Description: The Star Wars franchise depicts the adventures of characters "a long time ago in a galaxy far, far away" across multiple fictional eras, in which humans and many species of aliens (often humanoid) co-exist with droids, which may be programmed for personal assistance or battle.

Movie Name: The Exorcist
Description: The story chronicles a single mother's struggle to save her daughter from a mysterious ailment, later revealed to be demonic possession. She enlists the help of two Roman Catholic priests, who attempt to perform an exorcism.

Movie Name: Harry Potter
Description: The story begins when 11-year-old orphan Harry discovers that his parents were wizards and he starts his education in magic at Hogwart's School of Witchcraft and Wizardry. There he makes two close friends, Ron and Hermione, who share his adventures.

Movie Recommendation: {movie}
Movie Description:"""

    # Call the Cohere Chat endpoint
    response = co.chat( 
            messages=[{"role": "user", "content": prompt}],
            model="command-r-plus-08-2024", 
            temperature=0.5)
        
    return response.message.content[0].text

st.title('''🎬:red[CineMatch]🎬''')
st.subheader("Welcome to :red[CineMatch]! I am here to help recommend movies that are suitable to your preferences!", divider="red")

form = st.form(key="user_settings")
with form:
# User input - Genre name
    genre_input = st.multiselect(
    "Genre of Interest",
    ["Action", "Fantasty", "Adventure", "Horror", "Documentary", "Others"], default=None
)
    
st.write("You selected:", genre_input)

# Create a two-column view
col1, col2 = st.columns(2)

with col1:
    # User input - The number of movies to generate
    num_input = st.slider("Number of movies", value = 3, key = "num_input", min_value=1, max_value=10)

with col2:
    # User input - The 'temperature' value representing user's age
    age_input = st.slider("Age", value = 50, key = "age_input", min_value=0, max_value=100)

# Submit button to start generating movies
generate_button = form.form_submit_button("Generate Movies")

if generate_button:
    if genre_input == None:
        st.error("Genre of interest field cannot be blank")
    else:
        my_bar = st.progress(0.05)
        st.subheader("Movies Recommended For You")
        existing_movies = []
        for i in range(num_input):
            st.markdown("""---""")
            movie_recommendation = generate_unique_movies(genre_input, age_input, existing_movies)
            movie_description = generate_description(movie_recommendation,age_input)
            st.write(movie_recommendation)
            st.markdown("##### " + movie_description)
            my_bar.progress((i+1)/num_input)


