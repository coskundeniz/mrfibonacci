#!/usr/bin/env python3

import os
import sys
import time
import logging

try:
    import tweepy
except ImportError:
    print("Please run 'pipenv install' or 'pip install -r requirements.txt'")
    sys.exit(1)

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s, %(levelname)5s >>> %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(console_logger)


def fibonacci(n):
    """Calculate the nth fibonacci number.

    :type n: int
    :param n: index of fibonacci number to calculate
    :rtype: int
    :returns: nth fibonacci number
    """

    logger.info('Calculating fibonacci number for n = %s' % n)

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b

    return a


def generate_tweet_text(n, fibonacci_value):
    """Generate a text to send as tweet.

    If tweet length exceeds the Twitter limit,
    split it to multiple tweets.

    :type n: int
    :param n: index of fibonacci number
    :type fibonacci_value: int
    :param fibonacci_value: result of fibonacci(n)
    :rtype: str/tuple
    :returns: string if length of tweet is less than limit 
        or in parts as tuple
    """

    str_fib = str(fibonacci_value)
    tweet_text = '{} for n = {}'.format(fibonacci_value, n)

    logger.info('tweet_text: %s' % tweet_text)

    if len(str_fib) > 260:
        partial_tweet_text = []
        for part in range(len(tweet_text) // 260):
            partial_tweet_text.append(tweet_text[part*260:(part+1)*260])

        remaining = len(tweet_text) % 260
        if remaining:
            partial_tweet_text.append(tweet_text[-remaining:])

        return tuple(partial_tweet_text)
    else:
        return tweet_text


def setup_api_access():
    """Setup access and return twitter api wrapper.

    :rtype: tweepy.API
    :returns: Twitter API wrapper
    """

    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    return api


def send_tweet(tweet_text):
    """Send the tweet for nth fibonacci number.
    
    If tweet length is bigger than the Twitter limit, send
    multiple tweets.

    :type tweet_text: str or tuple
    :param tweet_text: Text to send as tweet
    """

    api = setup_api_access()
    is_multipart = isinstance(tweet_text, tuple)

    try:
        if is_multipart:
            logger.info('Multiple tweets. Sleep 5 seconds between tweets.')
            for tweet in tweet_text:
                status = api.update_status(tweet)
                time.sleep(5)
        else:
            status = api.update_status(tweet_text)

    except tweepy.TweepError as err:
        msg = 'Code: {}\nError: {}'
        logger.error(msg.format(err.args[0][0]['code'], err.args[0][0]['message']))
        sys.exit(1)

    else:
        logger.info('Created at: {}'.format(status._json['created_at']))
        logger.info('ID: {}'.format(status._json['id']))

  
def get_where_we_left():
    """Read the n value from file to calculate nth fibonacci number.

    :rtype: int
    :returns: Index to calculate fibonacci number
    """

    with open('where_we_left.txt') as fd:
        n = int(fd.read().strip())

    logger.debug('Read n from file as {}'.format(n))

    return n


def set_where_we_left(n):
    """Save the next n value to look for calculating fibonacci number.

    :type n: int
    :param n: Value of current index of calculation
    """

    n += 1

    logger.debug('Writing {} to file as next n value'.format(n))

    with open('where_we_left.txt', 'w') as fd:
        fd.write(str(n))


def main():
    """Read n from file, calculate nth fibonacci number,
    send tweet, and write next n to file.
    """
    
    n = get_where_we_left()
    nth_fibonacci_number = fibonacci(n)
    tweet_text = generate_tweet_text(n, nth_fibonacci_number)
    send_tweet(tweet_text)
    set_where_we_left(n)


if __name__ == '__main__':

    main()
