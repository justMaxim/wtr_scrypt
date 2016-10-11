from sets import Set
#from enum import Enum

from datetime import date
from datetime import datetime
from datetime import timedelta

class State:
    NONE = 0
    DATES = 1#start or end date entered
    RELATIVE = 2#-c, -p or -n key entered

Weeks = []
curentDate = datetime.now()
wtr_date = ""
wtr_second_date = ""

def addWeek(week):
	weekName = '%d-W%d' % (curentDate.year, week)
	Weeks.append(weekName)
	
def dateMatch(date):
	if re.match("^201\d-[01]\d-[0123]\d$", date):
   		print "date ok"
   		return True
	else:
		return False
	
def parseArgs(nextArg):#return int[0 : OK; -1 : ERROR ]
    if len(sys.argv) < (nextArg + 1):
        raise "ERROR: lack of arguments"
    state = State.NONE
    kyeSet = Set()
    current_week = curentDate.isocalendar()[1]
	
	
    for i in range(nextArg, len(sys.argv)) :
        arg = sys.argv[i]
        
        if arg == '-start':#Begin date
            if state == State.RELATIVE:
                raise "ERROR: botr keys[-c | -p | -n] and dates entered"
            
            if dateMatch(sys.argv[i + 1]):
                wtr_date = sys.argv[i + 1]
                i++
            else raise "ERROR: -start and -end must me followed by date"
            state = State.DATES
            
        elif arg == '-end':#End date
            if state == State.RELATIVE:
                raise "ERROR: botr keys[-c | -p | -n] and dates entered"
            
            if dateMatch(sys.argv[i + 1]):
                wtr_date = sys.argv[i + 1]
                i++
            else raise "ERROR: -start and -end must me followed by date"
            state = State.DATES
            
        elif arg in ['-c', '-p', '-n']:#Relative week number(from now)
            
            if state = State.Dates:
                raise "ERROR: botr keys[-c | -p | -n] and dates entered" 
                #ERROR
            
            if arg in keySet:
                raise "ERROR: twise keys " + arg

            keySet.add(arg)
			
            if arg == '-c':
                addWeek(current_week)
            elif arg == '-p':
                addWeek(current_week - 1)
            elif arg == '-n':
                addWeek(current_week + 1) 
                
        elif arg == -x:#Confirm instead of store as private
            
            if arg in keySet:
                raise "ERROR: twise keys " + arg
