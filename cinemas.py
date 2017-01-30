import heapq
import unicodedata
import time
from string import Formatter

from bs4 import BeautifulSoup
import requests


NUMBER_OF_BEST_MOVIES = 10


def get_raw_html(url):
    return requests.get(url).text

def parse_numbers_of_cinemas(afisha_html, number_of_movies=None):
    numbers_of_cinemas = {}
    soup = BeautifulSoup(afisha_html, 'html.parser')
    movies_divs = soup.find_all('div', class_='m-disp-table')
    for num_of_parsed_movies, div in enumerate(movies_divs):
        if number_of_movies and (num_of_parsed_movies >= number_of_movies):
            break
        title = div.h3.a.string
        schedule_html = div.find_next('table')
        number = len(schedule_html.find_all('td', class_='b-td-item'))
        numbers_of_cinemas[title] = number
    return numbers_of_cinemas

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

def parse_rating_info(movie_page_html):
    soup = BeautifulSoup(movie_page_html, 'html.parser')
    div = soup.find('div', id='block_rating')
    if div:
        average_rating = div.find('span', class_='rating_ball')
        number_of_ratings = div.find('span', class_='ratingCount')
        if average_rating and number_of_ratings:
            number_of_ratings = unicodedata.normalize("NFKD", number_of_ratings.text)
            return (float(average_rating.text), number_of_ratings)
    return (None, None)

def is_film_for_mass_market(number_of_cinemas, min_num_of_cinemas=25):
    return number_of_cinemas > min_num_of_cinemas

def get_mass_market_movies(numbers_of_cinemas):
    return [movie for movie, n in numbers_of_cinemas.items()
            if is_film_for_mass_market(n)]

def get_movies_pages_from_kinopoisk(movies):
    movies_pages = {}
    for title in movies:
        movies_pages[title] = get_movie_page_from_kinopoisk(title)
    return movies_pages

def get_rating_from_info(movie_info):
    rating = movie_info['rating']
    return (rating if rating else 0.0)

def get_ratings_from_pages(movies_pages):
    ratings = {}
    for title, page in movies_pages.items():
        ratings[title] = parse_rating_info(page)
    return ratings

def get_full_info(movies, ratings, numbers_of_cinemas):
    for title in movies:
        rating, ratings_counter = ratings[title]
        yield {'title':title,
               'rating':rating,
               'number of ratings':ratings_counter,
               'number of cinemas':numbers_of_cinemas[title]}


def main():
    afisha_schedule = 'http://www.afisha.ru/msk/schedule_cinema/'
    afisha_html = get_raw_html(afisha_schedule)

    numbers_of_cinemas = parse_numbers_of_cinemas(afisha_html)
    movies = get_mass_market_movies(numbers_of_cinemas)
    movies_pages = get_movies_pages_from_kinopoisk(movies)
    ratings = get_ratings_from_pages(movies_pages)

    movies_info = get_full_info(movies, ratings, numbers_of_cinemas)
    best_movies = heapq.nlargest(NUMBER_OF_BEST_MOVIES,
                                movies_info,
                                key=get_rating_from_info)
    output_template = (" • {title}"
                "\nRating: {rating:.2f}/10 (Total votes: {number of ratings})"
                "\nNumber of cinemas: {number of cinemas}")

    for movie in best_movies:
        print(output_template.format(**movie))

if __name__ == '__main__':
    main()
