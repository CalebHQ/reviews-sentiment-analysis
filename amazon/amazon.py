from bs4 import BeautifulSoup
import requests
import re
from textblob import TextBlob
from termcolor import colored
from progress.bar import Bar


def clean_data(data):
    cleaning = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    temp = []
    for review in data:
        review = review.text.strip()
        cleantext = re.sub(cleaning, '', review)
        temp.append(cleantext)
    return temp


def main():
    url = 'https://www.amazon.com.au/AMD-Ryzen-3900X-Processor-100-100000023BOX/product-reviews/B07SXMZLP9/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    total_reviews = []

    polarity = 0

    positive = 0
    neutral = 0
    negative = 0

    page = url

    count = 50
    page_no = 1
    while page_no <= count:
        bar = Bar('Processing', max=count, suffix='%(percent)d%%')
        for i in range(count):
            response = requests.get(page)
            soup = BeautifulSoup(response.text, 'html.parser')

            data = soup.find_all('span', {'data-hook': 'review-body'})

            reviews = clean_data(data)

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

            total_reviews += reviews

            page_no += 1
            try:
                page = url + f'&pageNumber={page_no}'
            except:
                break

            bar.next()
        bar.finish()

    total = len(total_reviews)

    output(total, polarity, positive, negative, neutral)


def output(total, polarity, positive, negative, neutral):
    print('='*50)
    print('')
    print(f'Sentiment Analysis on {total} Product reviews')
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


if __name__ == '__main__':
    main()
