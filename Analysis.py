f = open('Final2.txt',"r")

lines = f.readlines()

from collections import Counter

time_list = []
name_list = []
artist_list = []
views_list = []
release_list = []
msm_list = [1000000]

for line in lines:
    words = line.split("|")
    
    time_list.append(words[1].rstrip())
    name_list.append(words[2].rstrip())
    artist_list.append(words[3].rstrip())
    views_list.append(words[4].rstrip())
    release_list.append(words[5].rstrip())

for i in range(1,len(time_list)):
    if 'AM' in time_list[i]:
        if time_list[i][:2] == '12':
            msm_list.append(int(time_list[i][3:5]))
        else:
            msm_list.append(60*int(time_list[i][:2])+int(time_list[i][3:5]))
    else:
        if time_list[i][:2] == '12':
            msm_list.append(int(time_list[i][3:5])+720)
        else:
            msm_list.append(60*int(time_list[i][:2])+int(time_list[i][3:5])+720)

for o in range(1,len(views_list)):
    views_list[o] = int(views_list[o].replace(",",""))

for x in range(1,len(name_list)):
    if name_list[x] == "ALL OF ME":
        print(msm_list[x])
