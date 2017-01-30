import heapq
import unicodedata
import time
from string import Formatter

from bs4 import BeautifulSoup
import requests


def get_raw_html(url):
    return requests.get(url).text

def get_movies_info_from_afisha(afisha_html):
    soup = BeautifulSoup(afisha_html, 'html.parser')
    for div in soup.find_all('div', class_='m-disp-table'):
        title = div.h3.a.string
        schedule_html = div.find_next('table')
        number_of_cinemas = len(schedule_html.find_all('td', class_='b-td-item'))
        yield title, number_of_cinemas

def get_movie_page_from_kinopoisk(movie_title, seconds_to_wait=10):
    kinopoisk_search_url = 'https://www.kinopoisk.ru/index.php'
    payload = {'first': 'yes', 'kp_query': movie_title}
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
                  'Gecko/20100101 Firefox/50.0')
    headers = {'User-Agent':user_agent}
    timeout = (5,5)
    request = requests.get(url=kinopoisk_search_url,
                           params=payload,
                           timeout=timeout,
                           headers=headers)
    time.sleep(seconds_to_wait) # To avoid ban
    return request.text

def get_rating_info(movie_page_html):
    soup = BeautifulSoup(movie_page_html, 'html.parser')
    div = soup.find('div', id='block_rating')
    if div:
        average_rating = div.find('span', class_='rating_ball')
        number_of_ratings = div.find('span', class_='ratingCount')
        if average_rating and number_of_ratings:
            number_of_ratings = unicodedata.normalize("NFKD", number_of_ratings.text)
            return float(average_rating.text), number_of_ratings
    return None, None

def get_movies_info(num_of_movies=None, is_rated=False, is_mass_market=False,
                    min_num_of_cinemas=25):
    movies_info = []
    afisha_schedule = 'http://www.afisha.ru/msk/schedule_cinema/'
    afisha_html = get_raw_html(afisha_schedule)
    afisha_movies_info = get_movies_info_from_afisha(afisha_html)

    for title, num_of_cinemas in afisha_movies_info:
        if num_of_movies and (len(movies_info) >= num_of_movies):
            break
        if is_mass_market and (num_of_cinemas < min_num_of_cinemas):
            continue
        movie_page = get_movie_page_from_kinopoisk(title)
        rating, ratings_counter = get_rating_info(movie_page)
        if is_rated and (not rating):
            continue
        movies_info.append({'title': title,
                      'number of cinemas': num_of_cinemas,
                      'rating': rating,
                      'number of ratings': ratings_counter})
    return movies_info

def get_rating(movies_info):
    rating = movies_info['rating']
    return (rating if rating else 0.0)

def main():
    number_of_best_movies = 10
    template = (" • {title}"
                "\nRating: {rating:2f}/10 (Total votes: {number of ratings})"
                "\nNumber of cinemas: {number of cinemas}")
    movies_info = get_movies_info(is_rated=True,
                                  is_mass_market=True)
    best_movies = heapq.nlargest(number_of_best_movies,
                                movies_info,
                                key=get_rating)
    for movie in best_movies:
        print(template.format(**movie))

if __name__ == '__main__':
    main()
