from sets import Set
from enum import Enum

from datetime import date
from datetime import datetime
from datetime import timedelta

RelativeWeek = False
DateDiaposone = False

Weeks = []
curentDate = datetime.now()

def addWeek(week):
	weekName = '%d-W%d' % (curentDate.year, week)
	Weeks.append(weekName)

class States(Enum):
	NONE = 0
	ONE_DATE = 1
	TWO_DATES = 2
	RELATIVE_WEEK = 3
	EXECUTE = 4
	END = 5
	ERROR = 6
	
def parseArgs(nextArg):
	if len(sys.argv) < (nextArg + 1):
		raise "ERROR: lack of arguments"
	state = States.NONE
	kyeSet = Set()
	current_week = curentDate.isocalendar()[1]
	
	
	for arg in sys.argv:#pass all the arguments
		if arg == '-x':
			if arg in keySet:
				#ERROR: duplicate keys
			stete = States.EXECUTE
			kyeSet.add(arg)
			
		elif arg in ['-c', '-p', '-n']:
			if arg in keySet
				#ERROR: duplicate keys
			state = States.RELATIVE_WEEK
			keySet.add(arg)
			
			if arg == '-c':
				addWeek(current_week)
			elif arg == '-p':
				addWeek(current_week - 1)
			elif arg == '-n':
				addWeek(current_week + 1)

