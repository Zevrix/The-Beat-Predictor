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
" 12:42PM"
def convertToEpoch(timeStr):
    start = timeStr.index(":")+1
    timeStr = timeStr[start:]
    hour = ""
    minute = timeStr[-4:-2]
    if timeStr[-2] == "P":
        hour = str(int(timeStr[-7:-5])+12)
    if len(hour) == 1:
        hour = "0"+hour
    elif hour == "24":
        hour = "12"
    elif hour == "12" and timeStr[-2] == "A":
        hour = "00"
        
    now = datetime.datetime.now()
    dateTime = str(now.day)+str(now.month)+str(now.year)+hour+minute
    pattern = '%d%m%Y%H%M'
    epoch = int(time.mktime(time.strptime(dateTime, pattern)))
    return epoch


def formatData():
    for x in range(len(songs)):
        songs[x] = songs[x].get_text().replace('"', '\\"').replace("'", "\\'")
        artists[x] = artists[x].get_text().replace('"', '\\"').replace("'", "\\'")
        times[x] = convertToEpoch(times[x].get_text())
        print(songs[x], artists[x], times[x])

def populate(x):
    sql = "INSERT INTO songs (song_artist, song_name, predict_time, first_play, last_play, plays) VALUES (\'"+artists[x]+"\',\'"+songs[x]+"\',0,"+str(times[x])+","+str(times[x])+",1);"
    cur.execute(sql)
    db.commit()

def update(x):
    cur.execute("SELECT * FROM songs WHERE song_name = \'"+songs[x]+"\';")
    data = cur.fetchall()

    new_plays = data[0][6]+1
    new_predict = int((times[x]-data[0][4])/new_plays + times[x])
    new_last_play = times[x]

    sql = "UPDATE songs SET plays="+str(new_plays)+", predict_time ="+str(new_predict)+",last_play="+str(new_last_play)+" WHERE song_name = \'"+songs[x]+"\';"
    cur.execute(sql)
    db.commit()

def predict():
    cur.execute("SELECT song_name, predict_time FROM songs;")
    data = cur.fetchall()
    now = time.time()
    for x in data:
        if x[1] < (now + 100) and x[1] > (now - 100):
            print(x[0])

def main():
    formatData()
    cur.execute("SELECT song_name FROM songs;")

    for x in cur.fetchall():
        currSongs.append(x[0].replace('"', '\\"').replace("'", "\\'"))

    cur.execute("SELECT last_play FROM songs ORDER BY last_play DESC;")
    data = cur.fetchall()

    if data != ():
        timeLimit = data[0][0]
    else:
        timeLimit = 0

    for x in range(len(songs)):
        if songs[x] not in currSongs:
            populate(x)
        elif times[x] > timeLimit:
            update(x)

    predict()

    db.close()


main()
