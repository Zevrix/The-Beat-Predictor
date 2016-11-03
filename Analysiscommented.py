f = open('Final.txt', "r")

lines = f.readlines()

# in the shell Counter(name_list) or any other list for that matter can be
# used to generate a list sorted by how many times an
from collections import Counter
# element occurs .. so for Counter(name_list) we get something like ('ALL
# OF ME' (58), 'FANCY' (57), etc.)
time_list = []
name_list = []
artist_list = []
views_list = []  # names are still obvious
release_list = []
date_list = []

# minutes since midnight June 19th ... it needs a placeholder because it
# doesn't have a title in the first spot like the other lists
msm_list = [0.11111111]

for line in lines:
    words = line.split("|")

    time_list.append(words[1].rstrip())
    name_list.append(words[2].rstrip())
    artist_list.append(words[3].rstrip())
    # popoulates the list from Final.txt with whitespace removed
    views_list.append(words[4].rstrip())
    release_list.append(words[5].rstrip())
    date_list.append(words[6].rstrip())

# creates a list with only unique songs by removing all the repeats from
# name_list
unique_list = list(set(name_list))
# the titles from Final.txt are also added to the list ... I just removed
# here for accuracy
unique_list.remove("Song Name:")

for i in range(1, len(time_list)):
    if 'AM' in time_list[i]:
        if time_list[i][:2] == '12':
            msm = int(time_list[i][3:5])
        else:
            msm = 60 * int(time_list[i][:2]) + int(time_list[i][3:5])
    else:
        if time_list[i][:2] == '12':
            msm = int(time_list[i][3:5]) + 720
        else:
            msm = 60 * int(time_list[i][:2]) + int(time_list[i][3:5]) + 720

    if int(date_list[i][0]) == 6:  # for working with dates before July 1st

        date_check = int(date_list[i][2:4])
        msm_list.append((date_check - 20) * 1440 + msm)  # populates msm_list

    elif date_list[i][3] == '/':  # for working with single digit dates

        if date_list[i][0] == '7':
            date_check = int(date_list[i][2])
            msm_list.append((date_check) * 1440 + 10 * 1440 + msm)
        if date_list[i][0] == '8':
            date_check = int(date_list[i][2])
            msm_list.append((date_check) * 1440 + 41 * 1440 + msm)
        if date_list[i][0] == '9':
            date_check = int(date_list[i][2])
            msm_list.append((date_check) * 1440 + 72 * 1440 + msm)
        if date_list[i][:2] == '10':
            date_check = int(date_list[i][3])
            msm_list.append((date_check) * 1440 + 102 * 1440 + msm)

    else:  # for working with dates in july/august with 2 digits

        if date_list[i][0] == '7':
            date_check = int(date_list[i][2:4])
            msm_list.append((date_check) * 1440 + msm + 14400)
        if date_list[i][0] == '8':
            date_check = int(date_list[i][2:4])
            msm_list.append((date_check) * 1440 + 41 * 1440 + msm)
        if date_list[i][0] == '9':
            date_check = int(date_list[i][2:4])
            msm_list.append((date_check) * 1440 + 72 * 1440 + msm)


predict_list = []  # this list is going to contain the predicted times for the songs in unique_list in msm format


def check_song(name):  # function to check all of the plays of a song in the shell, just type check_song('SONG NAME') if you want to check it (caps are important)
    for x in range(1, len(name_list)):
        if name_list[x] == name.upper():
            print("|" + time_list[x] + (10 - len(time_list[x])) * " " + "|" + name_list[x] + (40 - len(name_list[x])) * " " + "|" + artist_list[x] + (30 - len(artist_list[x])) * " " +
                  "|" + views_list[x] + (20 - len(views_list[x])) * " " + "|" + release_list[x] + (20 - len(release_list[x])) * " " + "|" + date_list[x] + (15 - len(date_list[x])) * " " + "|")

for j in range(len(unique_list)):  # loops through each value of unique_list

    name = unique_list[j]  # sets name to a single song
    temp_list = []  # will contain the msm for a specific song
    total = 0

    # so lets say the temp_list for a song looks like [1,3,7,9]
    #(3-1)+(7-3)+(9-7) are all added to total which is then divided by 3 in order to get 8/3 or 2.66666
    # judging by this little series we can predict that the next value in the list will be 9 + 2.66666 or 11.6666
    # that value is added to predict_list
    # the more data points I have the more accurate the prediction

    for x in range(1, len(name_list)):
        if name_list[x] == name:
            temp_list.append(msm_list[x])  # populates temp_list

    if len(temp_list) > 1:  # no point doing this for only 1 data point
        temp_list.sort()
        for i in range(len(temp_list) - 1):
            total = total + (temp_list[i + 1] - temp_list[i])
        predict_list.append(
            round(total / (len(temp_list) - 1) + temp_list[-1]))  # see above
    else:
        predict_list.append(1)

Predictions = []

# this goes through predict_list and prints out songs with their predicted
# times that are within a certain range of the latest time
for l in range(len(predict_list)):
    # so here all songs predicted to happen within 100min of the last song are
    if predict_list[l] > (max(msm_list) - 100) and predict_list[l] < (max(msm_list) + 100):
        # found ... I can increase/decrease the range, 100 seems to give about
        # 70-80% chance of the real song
        Predictions.append(
            [abs(predict_list[l] - max(msm_list)), predict_list[l], unique_list[l]])
        # being in the list
Predictions.sort()

for z in range(len(Predictions)):
    print(Predictions[z])


def predict_check(name):  # use this to check the prediction of a song so if a song not in the range is played I can type in predict_check('SONG NAME') to see
    # how early or late it is
    print(predict_list[unique_list.index(name.upper())])

print()
# prints the msm of the last song so i know what the current time is
print(max(msm_list))
input()
