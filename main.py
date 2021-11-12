with open("bus_stops_orange.txt", "r") as f:
    stopslinelist = f.readlines()
with open("orange_schedule.txt", "r") as f:
    timeslinelist = f.readlines()


# initializes variables
places = []
stops = []
times = []
stopsintimes = []
stopsdict = {}
timesdict = {}
busname = ""

# strips \n from end of lines
def stripLines(plist: list) -> list:
    for i in range(len(plist)):
        plist[i] = plist[i].strip()
    return plist


stopslinelist = stripLines(stopslinelist)
timeslinelist = stripLines(timeslinelist)


# takes first line with bus name off of the top of the file and stores it in bus name
busname = stopslinelist[0]
# changes linelist to only include lines with information
stopslinelist = stopslinelist[1:]
timeslinelist = timeslinelist[1:]


# separates each data point into places and stops
def separatePlacesStops(lines: list, p: list, s: list) -> None:
    for i in range(len(lines)):
        lines[i] = lines[i].split(":")
        p.append(stopslinelist[i][0])
        s.append(stopslinelist[i][1])


separatePlacesStops(stopslinelist, places, stops)


def separateStopsTimes(lines: list, s: list, t: list) -> None:
    for i in range(len(lines)):
        firstcolon = lines[i].index(":")
        s.append(lines[i][:firstcolon])
        t.append(lines[i][firstcolon+1:])


separateStopsTimes(timeslinelist, stopsintimes, times)


# creates a list out of stops string by splitting it on /
def parseSlashStrings(plist: list) -> list:
    for i in range(len(plist)):
        plist[i] = plist[i].split("/")
    return plist


stops = parseSlashStrings(stops)
times = parseSlashStrings(times)

# creates list with stop and rating inside a single stops list by splitting on .
def parseOnDot(plist: list) -> list:
    for i in range(len(plist)):
        for j in range(len(plist[i])):
            plist[i][j] = plist[i][j].split(".")
    return plist


stops = parseOnDot(stops)


# converts time from "00:00 PM" format to total minutes integer
def convertStringtoTime(timeString: str) -> int:
    output = 0
    timeList = timeString.split(" ")
    # "07:53", "PM"
    nightday = timeList[1]
    hoursMinutes = timeList[0].split(":")
    for i in range(len(hoursMinutes)):
        hoursMinutes[i] = int(hoursMinutes[i])
    hours = hoursMinutes[0]
    minutes = hoursMinutes[1]
    if nightday == "AM" and hours == 12 and minutes < 60:
        output = minutes
    elif nightday == "AM" and hours < 12 and minutes < 60:
        output = (hours*60) + minutes
    elif nightday == "PM" and hours == 12 and minutes < 60:
        output = (hours*60) + minutes
    elif nightday == "PM" and hours < 12 and minutes < 60:
        output = ((hours+12)*60) + minutes
    else:
        print("Data error")
    return output

def convertTimetoString(time: int) -> str:
    hours = time // 60
    minutes = time % 60
    hourString = ""
    minuteString = ""
    nightDay = ""
    if hours == 0:
        hourString = "12"
        nightDay = "AM"
    elif hours == 12:
        hourString = "12"
        nightDay = "PM"
    elif hours > 12:
        hourString = str(hours-12)
        nightDay = "PM"
    elif hours < 12:
        hourString = str(hours)
        nightDay = "AM"
    else:
        print("Data error")

    if minutes == 0:
        minuteString = "00"
    elif minutes < 10:
        minuteString = "0" + str(minutes)
    else:
        minuteString = str(minutes)

    return hourString + ":" + minuteString + " " + nightDay


# converts all times in the times lists to integer numbers representing total minutes
def convertTimeListToInt(plist: list) -> list:
    for i in range(len(plist)):
        for j in range(len(plist[i])):
            plist[i][j] = convertStringtoTime(plist[i][j])
    return plist


def convertIntListToTime(plist: list) -> list:
    for i in range(len(plist)):
        for j in range(len(plist[i])):
            plist[i][j] = convertTimetoString(plist[i][j])
    return plist


times = convertTimeListToInt(times)


# matches every starting point to a stop list
def matchListsIntoDict(keys: list, items: list) -> dict:
    output = {}
    if len(keys) == len(items):
        for i in range(len(keys)):
            output[keys[i]] = items[i]
    return output


stopsdict = matchListsIntoDict(places, stops)
timesdict = matchListsIntoDict(stopsintimes, times)


# searches through pdict and retrieves what is held in key
def findItemInDict(key, pdict: dict):
    if key in pdict.keys():
        for i in pdict.keys():
            if i == key:
                return pdict[i]
    else:
        print("Invalid input")


def findClosestTime(stop: str, time: int) -> int:
    if stop in timesdict.keys():
        timelist = timesdict[stop]
        closestTime = 0
        for i in timelist:
            if i > closestTime and i < time:
                closestTime = i
        return closestTime
    else:
        print("Error")


#print(findItemInDict(str(input("Please input your starting point\n")), stopsdict))


def computeClosestTimes(starting: str, ending: str, arrivaltime: str) -> list:
    computedClosestArrTime = findClosestTime(findItemInDict(ending, stopsdict)[0][0], convertStringtoTime(arrivaltime))
    computedClosestDeptTime = findClosestTime(findItemInDict(starting, stopsdict)[0][0], computedClosestArrTime)
    return [computedClosestDeptTime, computedClosestArrTime]

start = str(input("Please input your starting point\n"))
destination = str(input("Please input your destination\n"))
inputtime = str(input("Please enter your arrival time\n"))
#computedClosestArrTime = convertTimetoString(findClosestTime(findItemInDict(destination, stopsdict)[0][0], convertStringtoTime(inputtime)))

times = computeClosestTimes(start, destination, inputtime)
print("Board bus at ", findItemInDict(start, stopsdict)[0][0], " at ", convertTimetoString(times[0]))
print("Exit bus at ", findItemInDict(destination, stopsdict)[0][0], " at ", convertTimetoString(times[1]))


