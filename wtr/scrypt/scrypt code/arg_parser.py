import re
from sets import Set

from datetime import date
from datetime import datetime
from datetime import timedelta

class State:
    NONE = 0
    DATES = 1#start or end date entered
    RELATIVE = 2#-c, -p or -n key entered

def addWeek(week):
	weekName = '%d-W%d' % (currentDate.year, week)
	Weeks.append(weekName)
	
def dateMatch(date):
	if re.match("^201\d-[01]\d-[0123]\d$", date):
   		return True
	else:
		return False
		
def storeAsPrivate_Day(browser):
	print "Store as private day"

def register_Day(browser):
	print "Register day"
	
def storeAsPrivate_Week(browser, firstDay, lastDay):
	print "Store week"

def register_Week(browser, firstDay, lastDay):
	print "Register week"   
	
def parseArgs(nextArg):#return int[0 : OK; -1 : ERROR ]
    global sys
    global wtr_date
    global wtr_end_date
    global wtr_profile
    
    if len(sys.argv) < (nextArg + 1):
        raise Exception("ERROR: lack of arguments")
    state = State.NONE
    kyeSet = Set()
    current_week = currentDate.isocalendar()[1]
	
    i = nextArg
    while i < len(sys.argv):
        arg = sys.argv[i]
        print arg
        if arg == '-start':#Begin date
            if state == State.RELATIVE:
                raise Exception("ERROR: botr keys[-c | -p | -n] and dates entered")
            
            if dateMatch(sys.argv[i + 1]):
                wtr_date = sys.argv[i + 1]
                i += 1
            else: raise Exception("ERROR: -start and -end must me followed by date")
            state = State.DATES
            
        elif arg == '-end':#End date
            if state == State.RELATIVE:
                raise Exception("ERROR: botr keys[-c | -p | -n] and dates entered")
            
            if dateMatch(sys.argv[i + 1]):
                wtr_date = sys.argv[i + 1]
                i += 1
            else: raise Exception("ERROR: -start and -end must me followed by date")
            state = State.DATES
            
        elif arg == '-profile':
            wtr_profile = sys.argv[i + 1]#!!!!!NEEDS TO IMPLEMENT CHECKING
            i += 1
        elif arg in ['-c', '-p', '-n']:#Relative week number(from now)
            
            if state == State.DATES:
                raise Exception("ERROR: you can't enter both dates and keys -c, -n or -p")
                #ERROR
            
            if arg in keySet:
                raise Exception("ERROR: twise keys " + arg)

            keySet.add(arg)
			
            if arg == '-c':
                addWeek(current_week)
            elif arg == '-p':
                addWeek(current_week - 1)
            elif arg == '-n':
                addWeek(current_week + 1) 
                
        elif arg == '-x':#Confirm instead of store as private
            
            if arg in keySet:
                raise Exception("ERROR: twise keys " + arg)
            
            global registerDay
            global registerWeek
            registerDay = register_Day
            registerWeek = register_Week
            
        elif dateMatch(arg):
            raise Exception("ERROR: you must enter key -start or -end befor date")
            #as we do i += 1 when hit -start or -end
            
        else: raise Exception("ERROR: wrong input: " + arg)
            
        i += 1
            
Weeks = []
currentDate = datetime.now()

wtr_date = currentDate.strftime("%Y-%m-%d")
wtr_second_date = currentDate.strftime("%Y-%m-%d")
wtr_profile = ""
registerDay = storeAsPrivate_Day
registerWeek = storeAsPrivate_Week
keySet = Set()

class system:
    argv = []

sys = system()
	
sys.argv = ['-c','-p','-n','-profile', "day off"]

print "fuck"

parseArgs(0)

registerDay(1)
registerWeek(2,3,4)

print wtr_profile
print Weeks
print wtr_date + "  " + wtr_second_date
