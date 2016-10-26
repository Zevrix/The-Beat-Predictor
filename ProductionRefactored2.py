from bs4 import BeautifulSoup
import urllib.request

response = urllib.request.urlopen('http://indie88.com/music/song-history')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())

mydivs = soup.findAll("div", { "class" : "recently-played-song" })

for x in mydivs:
    print(x)
