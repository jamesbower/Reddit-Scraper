#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created by @JamesBower on 20 Dec 2017
twitter.com/jamesbower
Inspired from: cheesinglee @ https://gist.github.com/cheesinglee
"""

import praw
import time
from time import gmtime
from datetime import datetime
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

############ Append JSON output to daily file ############

filename = 'reddit_'+ time.strftime('%Y-%m-%d', time.gmtime()) + '.json'

f = open(filename,"a+")

##########################################################

AUTH_PARAMS = {
	'client_id': 'Left Blank',
	'client_secret': 'Left Blank',
	'password': 'Left Blank',
	'username': 'Left Blank',
	'user_agent': 'Reddit:Explorers:0.1 (by /u/blibblob)'}

POST_KEYS = ['name', 'url', 'title', 'created_utc', 'score', 'subreddit', 'domain', 'is_self', 'selftext_html', 'downs', 'ups']

SUBREDDITS = ['Put Subreddit Here']

SCRAPE_AUTHORS = True

processed_users = {}

def get_author_info(a):
	if a:
		if a.id in processed_users:
			return processed_users[a.id]
		else:
			d = {}
			d['author_name'] = a.name
			t = gmtime(a.created_utc)
			processed_users[a.id] = d
			return d
	else:
		return {'author_name':'',
				'author_created_sec_utc':None}

def process_post(post):
	d = {}
	postdict = vars(post)
	for key in POST_KEYS:
		val = postdict[key]
		try:
			val = val.lower()
		except:
			pass
		d[key] = val

	d['has_thumbnail'] = (post.thumbnail != 'default') and (post.thumbnail != 'self')
	if d['has_thumbnail']:
		d['image_url'] = post.preview['images'][0]['source']['url']

############# Comment scraping ##########################
	post.comments.replace_more(limit=1)
	comments = post.comments.list()
	d['n_comments'] = len(list(comments))
	d['comments'] = list(map(lambda x: x.body, comments))
	#d['comments'] = list(map(comments))
#########################################################

############## Author scraping ##########################
	if SCRAPE_AUTHORS:
		author_dict = get_author_info(post.author)
		for key,val in author_dict.items():
			d[key] = val
	del d['subreddit']
#########################################################

############# Print output to screen for debugging ######

	#print(json.dumps(d))
    
#########################################################

############## Output JSON to file ######################
	
	f.write(json.dumps(d)+'\n')

#########################################################    		

if __name__ == '__main__':
	r = praw.Reddit(**AUTH_PARAMS)

	# posts = {post_id: post_content}
	posts = {}

	if len(SUBREDDITS) > 0:

		for subreddit in SUBREDDITS:

			sub = r.subreddit(subreddit)

			for post in sub.new(limit=1):
				if post.id not in posts:
					#print(post.title)
					posts[post.id] = process_post(post)

				#print('scraping hot posts...')
			#for post in sub.hot(limit=5):
				#if post.id not in posts:
						#print(post.title)
					#posts[post.id] = process_post(post)

	else:
		print('Choose a subreddit ...')
		sys.exit(0)
