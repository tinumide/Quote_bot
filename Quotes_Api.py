import  json
import requests

def get_quotes():
	# search_term = Quotes
	response = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1')
	r = response.json()[0]
	text = r['content'].replace('<p>', '').replace('</p>', '')
	# print(text)
	return text
	
	# filter[orderby]=rand&filter[posts_per_page]=1
	#response = requests.get('https://talaikis.com/api/quotes/random/.json')

	# print (response.text)
	# print(response.content)
	# data = response.json()
	# data = response.json()
	# return data


if __name__ == '__main__':
	print(get_quotes())

