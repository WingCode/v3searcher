from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import tweepy
from tweepy import OAuthHandler
import json, requests
import threading
import json

google_result=[None,"Resource not available"]
twitter_result=["Resource not available"]
duck_result=[None,"Resource not available"]

def main_thread(keyword=None):
	g_thread = threading.Thread(name='google_thread', target=google_searcher,args=(keyword,))
	g_thread.setDaemon(True)
	d_thread = threading.Thread(name='duck_thread', target=duck_searcher,args=(keyword,))
	d_thread.setDaemon(True)
	t_thread = threading.Thread(name='twitter_thread', target=twitter_searcher,args=(keyword,))
	t_thread.setDaemon(True)

	g_thread.start()
	t_thread.start()
	d_thread.start()

	g_thread.join()
	t_thread.join()
	d_thread.join()


def twitter_searcher(keyword=None):
	access_token = '3299388674-cHlogTHGBcXH4xZxgvftvXomneuuYVRRbd4ATx5'
	access_secret = 'ZCp2wLIQt45a5VOXIGmxWua9XsI330FvmWuQxrQgRExED'
	consumer_key = 'nDoNdJoIcUC5hNeXlVZ8kiBnh'
	consumer_secret = '8HJulUAQZu7r6VEkptgateAmMqfJ10Pt7ZK7gcga4VunJG81lH'
 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
 
	api = tweepy.API(auth)
	query = 'python'
	for tweet in tweepy.Cursor(api.search,q=keyword).items(1):
		final_result_twitter=tweet.text
	twitter_result[0]=final_result_twitter

def google_searcher(keyword=None):
	url="https://www.googleapis.com/customsearch/v1?key=AIzaSyANJy6pmMe1B4DB4QmLelV4FGYru7WG6do&cx=017576662512468239146:omuauf_lfve&q="
	url=''.join((url,keyword))
	google_result[0]=url
	resp = requests.get(url=url)
	data = json.loads(resp.text)
	google_result[1]=data['items'][0]['snippet']

def duck_searcher(keyword=None):
	url="http://api.duckduckgo.com/?q="
	url=''.join((url,keyword,"&format=json"))
	duck_result[0]=url
	resp = requests.get(url=url)
	data = json.loads(resp.text)
	duck_result[1]=data['Abstract']


# Create your views here.
def search(request,q=None):
	query = request.GET['q']
	query = query.replace('+',' ')

	m_thread = threading.Thread(name='main_thread', target=main_thread,args=(query,))
	m_thread.setDaemon(True)
	m_thread.start()
	m_thread.join(1)
	final_json=json.dumps({"query": query,"results": {"google": {"url": google_result[0],"text": google_result[1]},"twitter": {"url": "https://example.com?q="+query,"text": twitter_result},"duckduckgo": {"url": duck_result[0],"text": duck_result[1]}}},indent=4)
	return HttpResponse(final_json)