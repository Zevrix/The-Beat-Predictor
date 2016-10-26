from bs4 import BeautifulSoup
import urllib.request
import datetime
import time
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="Predictor")
cur = db.cursor()

response = urllib.request.urlopen('http://indie88.com/music/song-history')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

songs = soup.findAll("div", { "class" : "recently-played-song" })
artists = soup.findAll("div", { "class" : "recently-played-artist" })
times = soup.findAll("div", { "class" : "recently-played-time" })

currSongs = []

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


def formatData():
    for x in range(len(songs)):
        songs[x] = songs[x].get_text()
        artists[x] = artists[x].get_text()
        times[x] = convertToEpoch(times[x].get_text())
        print(songs[x], artists[x], times[x])

def populate(x):
    sql = "INSERT INTO songs (song_artist, song_name, predict_time, first_play, last_play, plays) VALUES (\'"+artists[x]+"\',\'"+songs[x]+"\',0,"+str(times[x])+","+str(times[x])+",1);"
    print(sql)
    cur.execute(sql)
    db.commit()


def main():
    formatData()
    cur.execute("SELECT song_name FROM songs")
    for x in cur.fetchall():
        currSongs.append(x[0])

    print(currSongs)

    for x in range(len(songs)):
        if songs[x] not in currSongs:
            populate(x)

    cur.execute("DELETE * FROM songs")
    db.commit()
    db.close()


main()
