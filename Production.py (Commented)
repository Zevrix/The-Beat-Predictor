import urllib.request
response = urllib.request.urlopen('http://www.thebeat.com/broadcasthistory.aspx') 
html = response.read()

html = str(html) #makes the html of the webpage where the beat displays their broadcast history usable

x = 0

time_list = []
minutes_list = []
name_list = []
artist_list = []
release_list = [] #most list names are self explanatory, minutes_list contains the number of minutes since midnight June 19th
views_list = []   

stop_list = [] #stop_list contains the minutes since midnight june 19th (msm) numbers for Final.txt which are stored in Stop.txt

stop = open('Stop.txt', 'r')

lines = stop.readlines()

for line in lines: #populates stop_list
    words = line.split("\n")
    stop_list.append(int(words[0]))
    
plsend = max(stop_list) #gets the max msm so the program knows that when minutes_list contains plsend we are adding songs which are already in Final.txt

def get_date(html): #gets date from the html
    end = '<option selected="selected" value="'
    html = html[html.index(end)+35:html.index(end)+43]
    return html

date = get_date(html)

def get_name_time(html):
    time = ""
    name = ""
    minutes = 0

    if ' AM' in html and ' PM' in html: #this chunk figures out how many minutes it has been since midnight on the specific date using the
        if html.index(' AM') < html.index(' PM'): #AM and PM data from the html
            time = html[html.index('AM')-6:html.index('AM')+2] #also gets time in string form
            if int(time[:2]) == 12:
                minutes = int(time[3:5])
            else:
                minutes = int(time[:2])*60+int(time[3:5])
        else:
            time = html[html.index('PM')-6:html.index('PM')+2]
            if int(time[:2]) == 12:
                minutes = int(time[:2])*60+int(time[3:5])
            else:
                minutes = int(time[:2])*60+int(time[3:5]) + 12*60
      
    elif ' AM' in html:
        time = html[html.index('AM')-6:html.index('AM')+2]
        if int(time[:2]) == 12:
            minutes = int(time[3:5])
        else:
            minutes = int(time[:2])*60+int(time[3:5])
            
    elif ' PM' in html:
        time = html[html.index('PM')-6:html.index('PM')+2]
        if int(time[:2]) == 12:
            minutes = int(time[:2])*60+int(time[3:5])
        else:
            minutes = int(time[:2])*60+int(time[3:5]) + 12*60

    minutes = int(date[2])*1440+minutes+72*1440 #uses the date to add however many days of minutes are needed in order to make minutes = to how many
                                               #minutes it has been since midnight June 19th
    html = html[html.index('        "')+9:]
    name_artist = html[:html.index('r\\n\\t\\t\\t')]
    name = name_artist[:html.index('"')] #this chunk gets song name and artist from html
    name = name.lstrip() #sometimes some whitespace is left behind so this is needed
    name_artist = name_artist[name_artist.index('-'):]
    artist = name_artist[2:name_artist.index('\\')]
    return [time,minutes,name,artist] #returns results as a list
        
while '<td class="timeStamp dim txtMini">' in html: #this line in the html comes before every song listing so my code depends on working around this
    
    html = html[html.index('<td class="timeStamp dim txtMini">')+34:] #each time this loop occurs the most recent iteration of the line is removed from the html

    if '</span>' in html: 
        
        end = html.index('</span>')

        L1 = get_name_time(html[:end]) #this isolates a little box of code in the html that has all the info i need so i can easily get it with my function

        time_list.append(L1[0])
        minutes_list.append(L1[1])
        name_list.append(L1[2]) #everything is added to its respective list
        artist_list.append(L1[3])

    else:

        end = html.index('</a>') #at the very last songs sometimes '</span>' won't work so this code is just here to avoid that error

        L1 = get_name_time(html[:end])

        time_list.append(L1[0])
        minutes_list.append(L1[1])
        name_list.append(L1[2])
        artist_list.append(L1[3])

    if minutes_list[-1] == plsend: #if the last value in minutes_list (the largest number basically) == the largest value in Stop.txt then that means
        break                      #we are at a point where adding any more songs would result in repeats so the loop is broken

    link = "https://www.youtube.com/results?search_query="+L1[2].replace(' ','+')+"+"+L1[3].replace(' ','+') 

    #the link searches song name + artist on youtube
    
    response2 = urllib.request.urlopen(link)
    youtube = response2.read()
    youtube = str(youtube)

    if youtube.count('views') >= 3:

        youtube = youtube[youtube.index("views")+5:]
        youtube = youtube[youtube.index("views")+5:]
        youtube = youtube[youtube.index("views")-100:youtube.index("views")]

    if youtube.count('views') != 2 and '"><li>' in youtube:

        release = youtube[youtube.index('"><li>')+6:]
        
        release_list.append(release[:release.index("</li><li>")])#the views and release date of the top result are added to their lists
        views_list.append(release[release.index("</li><li>")+9:])

    else:
        release_list.append("N/A")#sometimes it doesn't work 
        views_list.append("N/A")#i haven't tried fixing it because i'm not really using this data yet

    with open("Final.txt", "a") as text_file: #the data for this loop is added to Final.txt
        print("|"+time_list[x]+(10-len(time_list[x]))*" "+"|"+name_list[x]+(40-len(name_list[x]))*" "+"|"+artist_list[x]+(30-len(artist_list[x]))*" "+"|"+views_list[x]+(20-len(views_list[x]))*" "+"|"+release_list[x]+(20-len(release_list[x]))*" "+"|"+date+(15-len(date))*" "+"|", file = text_file)

    print("|"+time_list[x]+(10-len(time_list[x]))*" "+"|"+name_list[x]+(40-len(name_list[x]))*" "+"|"+artist_list[x]+(30-len(artist_list[x]))*" "+"|"+views_list[x]+(20-len(views_list[x]))*" "+"|"+release_list[x]+(20-len(release_list[x]))*" "+"|"+date+(15-len(date))*" "+"|")
    #it is also printed out in the shell

    x = x + 1 #x is increased so in the nth loop the nth values in the lists are added

with open("Stop.txt", "a") as text_file: 
    print(max(minutes_list), file = text_file) #minutes_list is added to Stop.txt so our stop point is updated for next time

print("...")
print("Final.txt has been updated.") #the end
input()
