from bs4 import BeautifulSoup
import urllib.request
import datetime
import time
import MySQLdb
import subprocess

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db="Predictor")
cur = db.cursor()

response = urllib.request.urlopen('http://indie88.com/music/song-history')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

songs = soup.findAll("div", {"class": "recently-played-song"})
artists = soup.findAll("div", {"class": "recently-played-artist"})
times = soup.findAll("div", {"class": "recently-played-time"})

currSongs = []


def convertToEpoch(timeStr):
    start = timeStr.index(":") + 1
    timeStr = timeStr[start:]
    hour = timeStr[-7:-5]
    minute = timeStr[-4:-2]
    if timeStr[-2] == "P":
        hour = str(int(hour) + 12)
    if len(hour) == 1:
        hour = "0" + hour
    elif hour == "24":
        hour = "12"
    elif hour == "12" and timeStr[-2] == "A":
        hour = "00"
    now = datetime.datetime.now()
    epoch = datetime.datetime(now.year, now.month, now.day, int(hour), int(minute)).timestamp()
    return epoch


def formatData():
    for x in range(len(songs)):
        songs[x] = songs[x].get_text().replace('"', '\\"').replace("'", "\\'")
        artists[x] = artists[x].get_text().replace(
            '"', '\\"').replace("'", "\\'")
        times[x] = convertToEpoch(times[x].get_text())


def populate(x):
    sql = "INSERT INTO songs (song_artist, song_name, predict_time, first_play, last_play, plays) VALUES (\'" + \
        artists[x] + "\',\'" + songs[x] + "\',0," + \
        str(times[x]) + "," + str(times[x]) + ",1);"
    cur.execute(sql)
    db.commit()
    outputToSlack(songs[x], times[x], 0)
    insertIntoPlays(x)


def update(x):
    cur.execute("SELECT * FROM songs WHERE song_name = \'" + songs[x] + "\';")
    data = cur.fetchall()
    print(data[0][1], times[x], data[0][3])
    outputToSlack(data[0][1], times[x], data[0][3])
    new_plays = data[0][6] + 1
    new_predict = int((times[x] - data[0][4]) / data[0][6] + times[x])
    new_last_play = times[x]

    sql = "UPDATE songs SET plays=" + str(new_plays) + ", predict_time =" + str(
        new_predict) + ",last_play=" + str(new_last_play) + " WHERE song_name = \'" + songs[x] + "\';"
    cur.execute(sql)
    db.commit()
    insertIntoPlays(x)


def predict():
    cur.execute("SELECT song_name, song_artist, predict_time FROM songs;")
    data = cur.fetchall()
    now = time.time()
    for x in data:
        if x[2] < (now + 1800) and x[2] > (now - 1800):
            pStr = time.strftime("%H:%M", time.localtime(x[2]))
            print(x[0], x[1], pStr)
            subprocess.call('sh ~/The-Beat-Predictor/slack.sh \"' +
                            x[0] + '\" \"' + x[1] + '\" \"' + pStr + '\"', shell=True)


def insertIntoPlays(x):
    song_id = findIDBySongName(songs[x])
    sql = "INSERT INTO plays (song_id, song_time) VALUES (" + \
        str(song_id) + ", " + str(times[x]) + ");"
    cur.execute(sql)
    db.commit()


def outputToSlack(songName, playTime, predictTime):
    playTime = time.strftime("%d %b %H:%M", time.localtime(playTime))
    if predictTime != 0:
        predictTime = time.strftime("%d %b %H:%M", time.localtime(predictTime))
    else:
        predictTime = "NULL"
    subprocess.call('sh ~/The-Beat-Predictor/plays.sh \"' + songName +
                    '\" \"' + playTime + '\" \"' + predictTime + '\"', shell=True)


def findIDBySongName(name):
    cur.execute("SELECT id FROM songs WHERE song_name = \'" + name + "\';")
    data = cur.fetchall()

    if data == ():
        print("Error: Song name not in songs table.")
        return 0
    else:
        return data[0][0]


def main():
    formatData()
    cur.execute("SELECT song_name FROM songs;")

    for x in cur.fetchall():
        currSongs.append(x[0].replace('"', '\\"').replace("'", "\\'"))

    cur.execute("SELECT last_play FROM songs ORDER BY last_play DESC;")
    data = cur.fetchall()

    if data != ():
        timeLimit = data[0][0]
        for x in range(len(times)):
            if times[x] - timeLimit > 80000:
                times[x] -= 86400
    else:
        timeLimit = 0

    print(timeLimit)
    for x in range(len(songs)):
        if songs[x] not in currSongs:
            populate(x)
        elif times[x] > timeLimit:
            update(x)

    predict()

    db.close()


main()
