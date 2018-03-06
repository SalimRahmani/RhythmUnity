from __future__ import print_function
import json
from datetime import datetime
from model import *

__author__ = 'Salim Rahmani'


def load_json(file):
    jsonfile = open(file)
    data = json.load(jsonfile)
    jsonfile.close()
    return data


def load_members(data):
    members = []
    for fullname in data:
        memberSchedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
        member = Member(fullname)
        for day in data[fullname]:
            for timeslot in data[fullname][day]:
                timeslot_tokenized = timeslot.split(" - ")
                timeslot = Timeslot(datetime.strptime(timeslot_tokenized[0], date_format), datetime.strptime(timeslot_tokenized[1], date_format))
                memberSchedule[day].append(timeslot)
        member.setSchedule(memberSchedule)
        members.append(member)
    return members


def load_bands(data):
    bands = []
    for band_name in data:
        bandsMembers = []
        band = Band(band_name)
        for member_name in data[band_name]:
            if get_member(member_name) is not None:
                bandsMembers.append(members[get_member(member_name)])
            else:
                print(member_name + " doesn't exist in the Members list! Please re-check!")
        band.members.extend(bandsMembers)
        bands.append(band)
    return bands


def get_member(fullname):
    for member in members:
        if(fullname == member.fullname):
            return members.index(member)


def get_general_schedule(members):
    schedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
    for member in members:
        for day in days:
            schedule[day].extend(member.schedule[day])
    schedule = check_schedule(schedule)
    return get_freetime_schedule(schedule)


def check_schedule(sched):
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


def get_bands_schedule(bands):
    for band in bands:
        bandSchedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
        bandSchedule = get_general_schedule(band.members)
        band.setSchedule(bandSchedule)


def print_schedule(sched):
    for day in days:
        print("\t" + day)
        for timeslot in sched[day]:
            print("\t\t" + datetime.strftime(timeslot.start, date_format) + " - " + datetime.strftime(timeslot.end, date_format))


def get_freetime_schedule(schedule):
    timeslot = Timeslot(datetime.strptime("08:00 AM", date_format), datetime.strptime("11:45 PM", date_format))
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
                    freeschedule[day].pop(i)
                    return 0
            i += 1
    return freeschedule


if __name__ == '__main__':

    date_format = "%I:%M %p"
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    schedule = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}

    print("-" * 80)
    print("Load the Json file: MembersSchedule.json")
    data = load_json('memberschedule.json')
    members = load_members(data)

    # 1-4 Generate the General Schedule
    schedule = get_general_schedule(members)
    print("The General Schedule: ")
    print_schedule(schedule)
    print("-" * 80)

    print("Load the Json file: Bands.json")
    data = load_json('bands.json')
    print("Loading bands: instance, schedule, and members list...\n")
    bands = load_bands(data)

    # 2-4 Generate Band Schedule based on members schedules
    get_bands_schedule(bands)

    for band in bands:
        print(band.name)
        print_schedule(band.schedule)
