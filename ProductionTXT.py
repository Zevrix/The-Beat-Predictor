import urllib.request

text_file = open("HTML.txt", "r")
html = text_file.read()
html = str(html)

x = 1

time_list = [1000000]
minutes_list = [1000000]
name_list = [1000000]
artist_list = [1000000]
release_list = [1000000]
views_list = [1000000]

with open("Output.txt", "a") as text_file:
    print("|"+"Time:"+" "*5+"|"+"Song Name:"+30*" "+"|"+"Artist:"+" "*23+"|"+"Youtube Views:"+6*" "+"|"+"Release Date:" + 7 * " " + "|"+"Play Date:" + 5*" "+"|", file = text_file)

def get_date(html):
    end = '<option selected="selected" value="'
    html = html[html.index(end)+35:html.index(end)+44]
    return html

date = get_date(html)

def get_name_time(html):
    time = ""
    name = ""
    minutes = 0

    if ' AM' in html and ' PM' in html:
        if html.index(' AM') < html.index(' PM'):
            time = html[html.index('AM')-6:html.index('AM')+2]
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

    html = html[html.index('<td class="broadcast txtMini" width="90%">'):]
    html = html[html.index('        "')+9:]
    html = html[:html.index('   ')]
    html = html.split(' - ')
    name = html[0][:-1]
    name = name.lstrip()
    artist = html[1][:html[1].index('\n')]

    return [time,minutes,name,artist]
        
while '<td class="timeStamp dim txtMini">' in html:
    
    html = html[html.index('<td class="timeStamp dim txtMini">')+34:]

    if '</span>' in html: 
        
        end = html.index('</span>')

        L1 = get_name_time(html[:end]) 

        time_list.append(L1[0])
        minutes_list.append(L1[1])
        name_list.append(L1[2]) 
        artist_list.append(L1[3])

    else:

        end = html.index('</a>') 

        L1 = get_name_time(html[:end])

        time_list.append(L1[0])
        minutes_list.append(L1[1])
        name_list.append(L1[2])
        artist_list.append(L1[3])

    link = "https://www.youtube.com/results?search_query="+L1[2].replace(' ','+')+"+"+L1[3].replace(' ','+')

    response2 = urllib.request.urlopen(link)
    youtube = response2.read()
    youtube = str(youtube)

    if youtube.count('views') >= 3:

        youtube = youtube[youtube.index("views")+5:]
        youtube = youtube[youtube.index("views")+5:]
        youtube = youtube[youtube.index("views")-100:youtube.index("views")]

    if youtube.count('views') != 2 and '</li><li>' in youtube:

        release = youtube[youtube.index('</li><li>')+9:]
        
        release_list.append(release[:release.index("</li><li>")])
        views_list.append(release[release.index("</li><li>")+9:])

    else:
        release_list.append("N/A")
        views_list.append("N/A")

    with open("Final.txt", "a") as text_file:
        print("|"+time_list[x]+(10-len(time_list[x]))*" "+"|"+name_list[x]+(40-len(name_list[x]))*" "+"|"+artist_list[x]+(30-len(artist_list[x]))*" "+"|"+views_list[x]+(20-len(views_list[x]))*" "+"|"+release_list[x]+(20-len(release_list[x]))*" "+"|"+date+(15-len(date))*" "+"|", file = text_file)

    print("|"+time_list[x]+(10-len(time_list[x]))*" "+"|"+name_list[x]+(40-len(name_list[x]))*" "+"|"+artist_list[x]+(30-len(artist_list[x]))*" "+"|"+views_list[x]+(20-len(views_list[x]))*" "+"|"+release_list[x]+(20-len(release_list[x]))*" "+"|"+date+(15-len(date))*" "+"|")

    x = x + 1
