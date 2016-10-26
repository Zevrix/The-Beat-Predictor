from bs4 import BeautifulSoup
import urllib.request
import datetime
import time

response = urllib.request.urlopen('http://indie88.com/music/song-history')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

songs = soup.findAll("div", { "class" : "recently-played-song" })
artists = soup.findAll("div", { "class" : "recently-played-artist" })
times = soup.findAll("div", { "class" : "recently-played-time" })
epochTimes = []

def convertToEpoch(timeStr):
    start = timeStr.index(":")+1
    timeStr = timeStr[start:]
    hour = 0
    minute = timeStr[-4:-2]
    if timeStr[-2] == "P":
        hour = str(int(timeStr[-7:-5])+12)
    if len(hour) == 1:
        hour = "0"+hour
    now = datetime.datetime.now()
    dateTime = str(now.day)+str(now.month)+str(now.year)+hour+minute
    pattern = '%d%m%Y%H%M'
    epoch = int(time.mktime(time.strptime(dateTime, pattern)))
    return epoch


for x in range(len(songs)):
    songs[x] = songs[x].get_text()
    artists[x] = artists[x].get_text()
    epochTimes.append(convertToEpoch(times[x].get_text()))
    print(songs[x], artists[x], times[x], epochTimes[x])
