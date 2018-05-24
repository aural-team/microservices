import requests
from bs4 import BeautifulSoup

def asciify(text):
	asciified_text = ''
	for t in text:
		if ord(t) < 128:
			asciified_text += t
	return asciified_text

def scrape_in_shorts():
	url = "https://inshorts.com/read"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')

	rows = soup.findAll('div', attrs = {'class': 'news-card-content'})
	articles = []
	for row in rows:
		article = row.get_text().split("\n")[1].strip().replace("(", "").replace(")", "")
		articles.append(asciify(article))
	return articles


if __name__ == "__main__":
	articles = scrape_in_shorts()
	for article in articles:
		print article + "\n"
