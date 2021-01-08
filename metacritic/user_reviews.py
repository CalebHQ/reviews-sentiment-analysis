from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from textblob import TextBlob
from termcolor import colored
from time import sleep


class UserReviews:
    def __init__(self, movie, url):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--incognito")
        self.options.add_argument("--headless")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.movie = movie
        self.url = url
        self.total_reviews = []
        self.polarity = 0
        self.positive = 0
        self.neutral = 0
        self.negative = 0
        self.page = 0

    def clean_data(self):
        self.reviews = []
        cleaning = re.compile(
            '<.*?>|-&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        for review in self.data:
            review = review.text.strip()
            cleantext = re.sub(cleaning, '', review)
            self.reviews.append(cleantext)

        self.total_reviews += self.reviews

    def get_data(self):
        self.driver.get(self.url)
        try:
            self.last_page = self.driver.find_element_by_xpath(
                '//*[@id="main_content"]/div[1]/div[3]/div/div[1]/div[7]/div/div[2]/ul/li[last()]/a').text
        except NoSuchElementException:
            print(colored('Last Page Reached', 'blue'))
        self.data = self.driver.find_elements_by_xpath(
            '//div[@class="summary"]')

        return self.data

    def get_polarity(self):
        for review in self.reviews:
            self.analysis = TextBlob(review)
            review_polarity = self.analysis.polarity
            if review_polarity > 0:
                self.positive += 1
            elif review_polarity <= 0:
                self.negative += 1
            elif review_polarity == 0:
                self.neutral += 1
            self.polarity += review_polarity

        return self.polarity

    def next_page(self):
        self.page += 1
        self.url = f'https://www.metacritic.com/movie/{movie}/user-reviews?page={self.page}'

    def get_last_page(self):
        return int(self.last_page)

    def get_current_page(self):
        return self.page

    def get_reviews(self):
        return self.total_reviews

    def output(self):
        self.total = len(self.total_reviews)
        print('='*50)
        print('')
        print(f'Sentiment Analysis on {self.total} Critic reviews')
        print('')
        print(f'Polarity: {self.polarity:.2f}')
        if self.polarity > 0:
            print(colored("{0:.0f}% Positive".format(
                self.positive/self.total * 100), 'green'))
        elif self.polarity <= 0:
            print(colored("{0:.0f}% Negative".format(
                self.negative/self.total * 100), 'red'))
        elif self.polarity == 0:
            print(colored("{0:.0f}% Neutral".format(
                self.neutral/self.total * 100), 'blue'))
        print('')
        print(colored(f'Positive Reviews: {self.positive}', 'green'))
        print(colored(f'Negative Reviews: {self.negative}', 'red'))
        print(colored(f'Neutral Reviews: {self.neutral}', 'blue'))
        print('')
        print('='*50)


if __name__ == '__main__':
    movie = input(colored('Enter Movie: ', 'blue')).replace(' ', '-').lower()
    url = f'https://www.metacritic.com/movie/{movie}/user-reviews?page=0'

    mc = UserReviews(movie, url)

    while True:
        sleep(1)
        mc.get_data()
        mc.clean_data()
        mc.get_polarity()
        print(colored(f'Page {mc.get_current_page()+1} Complete', 'red'))
        mc.next_page()
        if mc.get_last_page() == mc.get_current_page():
            break

    mc.output()
