import json
from pprint import pprint

with open('reddit_2017_01_posts.json') as data_file:    
    reddit_posts = json.load(data_file)

pprint(reddit_posts)
