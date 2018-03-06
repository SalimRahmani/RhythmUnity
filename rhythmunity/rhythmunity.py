import json
from datetime import datetime
from model import *
from __future__ import print_function


__author__ = 'Salim Rahmani'


def loadJSON(file):
    jsonfile = open(file)
    data = json.load(jsonfile)
    jsonfile.close()
    return data


def loadsMembers(data):
    members = []
    for fullname in data:
        memberSchedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
        member = Member(fullname)
        for day in data[fullname]:
            for timeslot in data[fullname][day]:
                timeslot_tokenized = timeslot.split(" - ")
                timeslot = Timeslot(datetime.strptime(timeslot_tokenized[0], format), datetime.strptime(timeslot_tokenized[1], format))
                memberSchedule[day].append(timeslot)
        member.setSchedule(memberSchedule)
        members.append(member)
    return members


def loadsBands(data):
    bands = []
    for band_name in data:
        bandsMembers = []
        band = Band(band_name)
        for member_name in data[band_name]:
            if getMember(member_name) is not None:
                bandsMembers.append(members[getMember(member_name)])
            else:
                print(member_name + " doesn't exist in the Members list! Please re-check!")
        band.members.extend(bandsMembers)
        bands.append(band)
    return bands


def getMember(fullname):
    for member in members:
        if(fullname == member.fullname):
            return members.index(member)


def generalSchedule(members):
    schedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
    for member in members:
        for day in days:
            schedule[day].extend(member.schedule[day])
    schedule = checkSchedule(schedule)
    return freetimeschedule(schedule)


def checkSchedule(sched):
    for day in days:
        i = 0
        sched[day] = sorted(sched[day], key=lambda timeslot: (timeslot.start, timeslot.end))
        while(i < len(sched[day])-1):
            if (sched[day][i].end >= sched[day][i+1].end):
                sched[day].pop(i+1)
                i = i-1
            elif (sched[day][i].end >= sched[day][i+1].start) and (sched[day][i].end < sched[day][i+1].end):
                sched[day][i].end = sched[day][i+1].end
                sched[day].pop(i+1)
                i = i-1
            i += 1
    return sched


def bandsSchedule(bands):
    for band in bands:
        bandSchedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
        bandSchedule = generalSchedule(band.members)
        band.setSchedule(bandSchedule)


def printschedule(sched):
    for day in days:
        print("\t" + day)
        for timeslot in sched[day]:
            print("\t\t" + datetime.strftime(timeslot.start, format) + " - " + datetime.strftime(timeslot.end, format))


def freetimeschedule(schedule):
    timeslot = Timeslot(datetime.strptime("08:00 AM", format), datetime.strptime("11:45 PM", format))
    freeschedule = {"Monday": [timeslot], "Tuesday": [timeslot], "Wednesday": [timeslot], "Thursday": [timeslot]}
    for day in days:
        i = 0
        while (i <= len(freeschedule[day])-1):
            for timeslot in schedule[day]:
                if (timeslot.start > freeschedule[day][i].start) and (timeslot.end < freeschedule[day][i].end):
                    tms_one = Timeslot(freeschedule[day][i].start, timeslot.start)
                    tms_two = Timeslot(timeslot.end, freeschedule[day][i].end)
                    freeschedule[day].pop(i)
                    freeschedule[day].extend([tms_one, tms_two])
                    i -= 1
                if (timeslot.start == freeschedule[day][i].start) and (timeslot.end < freeschedule[day][i].end):
                    tms_one = Timeslot(timeslot.end, freeschedule[day][i].end)
                    freeschedule[day].pop(i)
                    freeschedule[day].append(tms_one)
                    i -= 1
                if (timeslot.start > freeschedule[day][i].start) and (timeslot.end == freeschedule[day][i].end):
                    tms_one = Timeslot(freeschedule[day][i].start, timeslot.start)
                    freeschedule[day].pop(i)
                    freeschedule[day].append(tms_one)
                    i -= 1
                if (timeslot.start <= freeschedule[day][i].start) and (timeslot.end >= freeschedule[day][i].end):
                    # remove
                    freeschedule[day].pop(i)
                    return 0
                    # break
            i += 1
    return freeschedule


if __name__ == '__main__':
    # 0- Global Variables
    format = "%I:%M %p"
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    schedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}

# ------------------------------------------------------------------------------------------------------------------------
# 1- Load All Members
    # 1-1 Load JSON file
    print("-" * 80)
    print("Load the Json file: MembersSchedule.json")
    data = loadJSON('memberschedule.json')
    # 1-2 Initialize Members
    print("Loading members: instance, schedule, and members list...\n")
    members = loadsMembers(data)
    '''
    # 1-3 Print Each Member's schedule
    print "Print Each Member's schedule"
    for member in members:
        print member.fullname
        printschedule(member.schedule)
    print "-" * 80
    '''
    # 1-4 Generate the General Schedule
    schedule = generalSchedule(members)
    print("The General Schedule: ")
    printschedule(schedule)
    print("-" * 80)

# ------------------------------------------------------------------------------------------------------------------------
# 2- Load Bands
    # 2-1 Load JSON file
    print("Load the Json file: Bands.json")
    data = loadJSON('bands.json')
    # 2-2 Initialize Bands
    print("Loading bands: instance, schedule, and members list...\n")
    bands = loadsBands(data)
    '''
    # 2-3 Print the schedule of each band's member
    for band in bands:
        print band.name
        for member in band.members:
            print "\t" + member.fullname
            printschedule(member.schedule)
    print "-" * 80
    '''
    # 2-4 Generate Band Schedule based on members schedules
    bandsSchedule(bands)
    # 2-5 Print each band's schedule
    for band in bands:
        print(band.name)
        printschedule(band.schedule)
# ------------------------------------------------------------------------------------------------------------------------
