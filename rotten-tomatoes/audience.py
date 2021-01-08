from selenium import webdriver
from time import sleep
import re
from selenium.common.exceptions import NoSuchElementException
from textblob import TextBlob
from termcolor import colored
from progress.bar import Bar

TIME = 1

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_experimental_option("detach", True)


def get_movie():
    print('')
    print('Enter Movie:')
    movie = input('> ')
    movie = movie.replace(' ', '_')
    print('')

    return movie


def clean_data(data):
    cleaning = re.compile('<.*?>|-&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    reviews = []
    for review in data:
        review = review.text.strip()
        cleantext = re.sub(cleaning, '', review)
        reviews.append(cleantext)

    return reviews


def output(polarity, positive, negative, neutral, total):
    print('='*50)
    print('')
    print(f'Sentiment Analysis on {total} Audience reviews')
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


def run():
    movie = get_movie()

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(f'https://www.rottentomatoes.com/m/{movie}/reviews?type=user')

    polarity = 0

    total_reviews = []

    positive = 0
    neutral = 0
    negative = 0

    count_max = 3
    count = 0

    while True:
        bar = Bar('Processing', max=count_max, suffix='%(percent)d%%')
        for i in range(count_max):
            data = driver.find_elements_by_xpath(
                '//p[@class="audience-reviews__review js-review-text clamp clamp-8 js-clamp"]')

            processed_data = clean_data(data)
            total_reviews += processed_data

            for review in processed_data:
                analysis = TextBlob(review)
                review_polarity = analysis.polarity
                if review_polarity > 0:
                    positive += 1
                elif review_polarity <= 0:
                    negative += 1
                elif review_polarity == 0:
                    neutral += 1
                polarity += review_polarity

            processed_data.clear()

            try:
                driver.find_element_by_xpath(
                    '//button[@data-direction="next"]').click()
            except NoSuchElementException:
                break

            count += 1

            sleep(TIME)

            bar.next()
        bar.finish()
        break

    total = len(total_reviews)

    print(total_reviews[0])
    print(total_reviews[-1])

    output(polarity, positive, negative, neutral, total)
