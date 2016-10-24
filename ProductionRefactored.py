import urllib2

response = urllib2.urlopen('http://indie88.com/music/song-history')
html = response.read()

start = html.index('class="recently-played"')
end = html.index('class="recently-played-back"')

html = html[start:end]

songData = {}


def getSongHTML(html):
    while 'class="recently-played-item"' in html:
        start = html.index('class="recently-played-song"')
        end = html.index('class=\"recently-played-buy-link')
        getSongData(html[start:end])
        getSongHTML(html[end:])

def getSongData(songHTML):
    songName = songHTML[songHTML.index(">")+1:songHTML.index("<")]
    songData[songName] = 0


getSongHTML(html)

print(songData)
