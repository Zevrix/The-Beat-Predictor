from bs4 import BeautifulSoup
import urllib.request

response = urllib.request.urlopen('http://indie88.com/music/song-history')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

songs = soup.findAll("div", { "class" : "recently-played-song" })
artists = soup.findAll("div", { "class" : "recently-played-artist" })
times = soup.findAll("div", { "class" : "recently-played-time" })

for x in range(len(songs)):
    print(songs[x])
    print(artists[x])
    print(times[x])
