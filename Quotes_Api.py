import  json
import requests

def get_quotes(Quotes):
	search_term = ''
	response = requests.get('' , search_term)
	data = response.json()
	


	if __name__ == '__main__':
		get_quotes()