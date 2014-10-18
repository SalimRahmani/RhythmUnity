class Timeslot:
	def __init__(self,start,end):
		self.start = start
		self.end = end

class Member:
	def __init__(self, fullname):
		self.fullname = fullname
		self.schedule = {}

	def setSchedule(self, schedule):
		self.schedule = schedule

class Band:
	def __init__(self, name):
		self.name = name
		self.schedule = {}
		self.members = []

	def assignMembers(self, members):
		self.members.extend(members)

	def setSchedule(self, schedule):
		self.schedule = schedule
