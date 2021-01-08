from bs4 import BeautifulSoup
import requests
import re
from textblob import TextBlob
from termcolor import colored
import sys
from progress.bar import Bar


def get_movie():
    print('')
    print('Enter Movie:')
    movie = input('> ')
    movie = movie.replace(' ', '_')
    print('')

    return movie


def get_url(movie):
    url = f'https://www.rottentomatoes.com/m/{movie}/reviews'
    return url


def get_page(movie):
    url = f'https://www.rottentomatoes.com/m/{movie}/reviews'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_count = soup.find('span', {'class': 'pageInfo'})

    page_numbers = []
    try:
        for char in page_count.text.split():
            if char.isdigit():
                page_numbers.append(int(char))
    except AttributeError:
        print(colored('Movie does not exist', 'red'))
        main()

    if page_numbers == []:
        page_numbers = [0, 0]

    last_page = page_numbers[1]
    return last_page


def clean_data(data):
    cleaning = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    reviews = []
    for review in data:
        review = review.text.strip()
        cleantext = re.sub(cleaning, '', review)
        reviews.append(cleantext)

    return reviews


def get_next_page(movie, page):
    url = f'https://www.rottentomatoes.com/m/{movie}/reviews?&page={page}'

    return url


def main():
    movie = get_movie()
    polarity = 0

    total_reviews = []

    positive = 0
    neutral = 0
    negative = 0

    last_page = get_page(movie)
    page = 1

    url = f'https://www.rottentomatoes.com/m/{movie}/reviews'

    while page <= last_page:
        bar = Bar('Processing', max=last_page, suffix='%(percent)d%%')
        for i in range(last_page):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            data = soup.find_all('div', {'class': 'the_review'})

            reviews = clean_data(data)
            total_reviews += reviews

            for review in reviews:
                analysis = TextBlob(review)
                review_polarity = analysis.polarity
                if review_polarity > 0:
                    positive += 1
                elif review_polarity <= 0:
                    negative += 1
                elif review_polarity == 0:
                    neutral += 1
                polarity += review_polarity

            reviews.clear()

            page += 1
            try:
                url = get_next_page(movie, page)
            except IndexError:
                print('')
                print(colored('Last Page Reached', 'red'))
                print('')
                break
            bar.next()
        bar.finish()

    total = len(total_reviews)

    if total > 1:
        output(polarity, positive, negative, neutral, total)

    sys.exit(colored('Goodbye!', 'red'))


def output(polarity, positive, negative, neutral, total):
    print('='*50)
    print('')
    print(f'Sentiment Analysis on {total} Critic reviews')
    print('')
    print(f'Polarity: {polarity:.2f}')
    if polarity > 0:
        print(colored("{0:.0f}% Positive".format(
            positive/total * 100), 'green'))
    elif polarity <= 0:
        print(colored("{0:.0f}% Negative".format(negative/total * 100), 'red'))
    elif polarity == 0:
        print(colored("{0:.0f}% Neutral".format(neutral/total * 100), 'blue'))
    print('')
    print(colored(f'Positive Reviews: {positive}', 'green'))
    print(colored(f'Negative Reviews: {negative}', 'red'))
    print(colored(f'Neutral Reviews: {neutral}', 'blue'))
    print('')
    print('='*50)
