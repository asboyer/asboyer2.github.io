import sys
import requests
import imdb 
import json

sys.path.append('secret')
from api_keys import tmdb_key as KEY

def imdb_title_from_search(query):
    ia = imdb.IMDb()
    
    search = ia.search_movie(query)

    return search[0]['title']


def imdb_id_from_title(title):
    ia = imdb.IMDb()
    
    search = ia.search_movie(title)

    return search[0].movieID

def get_movie_url(movie_title):
    CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
    
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])

    imdb_id = imdb_id_from_title(imdb_title_from_search(movie_title))

    url = CONFIG_PATTERN.format(key=KEY)
    r = requests.get(url)
    config = r.json()

    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']
    max_size = max(sizes, key=size_str_to_int)

    IMG_PATTERN = 'https://api.themoviedb.org/3/find/tt{imdbid}?api_key={key}&external_source=imdb_id'

    r = requests.get(IMG_PATTERN.format(key=KEY,imdbid=imdb_id))
    api_response = r.json()
    rel_path = api_response['movie_results'][0]['poster_path']
    url = "{0}{1}{2}".format(base_url, max_size, rel_path)
    return url

def update_movie_database():

    print('reading text file...')
    with open('data/movies.txt', 'r') as f:
        movies = f.readlines()

    print('reading current database...')
    with open('data/movies.json', 'r') as json_file:
        data = json.load(json_file)

        current_movies = list(data.keys())

        print('getting titles...')
        for i in range(len(movies)):
            movies[i] = imdb_title_from_search(movies[i])

        print('looping through movies...')
        for movie in movies:
            if movie not in current_movies:
                print(f'adding \'{movie}\'...') 
                # movie is in the list, but not present in the dictionary
                data[movie] = {}
                data[movie]['id'] = imdb_id_from_title(movie)
                data[movie]['image'] = get_movie_url(movie)

        print('checking titles for removed movies...')
        for movie_title in current_movies:
            if movie_title not in movies:
                print(f'removing \'{movie}\'...')
                data.pop(movie_title)

    print('saving database...')
    with open('data/movies.json', 'w') as json_file: 
        json.dump(data, json_file, indent=4)

    print('DATABASE UPDATED')

        

# EXTRA:

# DOWNLOADING IMG

# r = requests.get(url)
# filetype = r.headers['content-type'].split('/')[-1]
# filename = 'poster_{0}.{1}'.format(1,filetype) 
# with open(filename,'wb') as w:
#     w.write(r.content)

# help from: 
# https://johannesbader.ch/blog/tutorial-download-posters-with-the-movie-database-api-in-python/
# https://www.geeksforgeeks.org/python-imdbpy-getting-movie-id-from-searched-movies/