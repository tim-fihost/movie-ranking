import requests
link = "https://api.themoviedb.org/3/search/movie"
api_key = "8957d4218e6c655f84c7ff730e25d03d"
img_url = "https://image.tmdb.org/t/p/w500"

def search_movie(movie_name):
    movie_search_result = []
    response = requests.get(url=link, params={'api_key': api_key,'query':f"{movie_name}"})
    data = response.json()
    for movie in data['results']:
        result =  { 
        'title' : movie['title'],
        'description' : movie['overview'], 
        'year' : movie['release_date'],
        'img_url' : f"{img_url}/{movie['poster_path']}",
        'rating' : movie['vote_average'],
        'id' : movie['id']
        }
        movie_search_result.append(result)
    return movie_search_result
