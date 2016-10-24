#!/usr/bin/python
import re
import mechanize
import sys
import os.path
import webbrowser

from sets import Set

from datetime import date
from datetime import datetime
from datetime import timedelta

wtr_login = ""#in file login.py
wtr_password = ""

'''elif arg == Keys.EXACTLY:
			if arg in keySet:
				state = State.ERROR
				ERROR = "ERROR: twise keys " + arg
				break
			
			global AutoDayOFF
			AutoDayOFF = False'''

class Keys:
	START_DAY = "-date"
	END_DAY = "-sec"
	CURRENT_WEEK = "-c"
	PREVIOUS_WEEK = "-p"
	NEXT_WEEK = "-n"
	WEEK = "-week"
	PROFILE = "-profile"
	#EXACTLY = "-exactly"#auto day off = false
	EXECUTE = "-register"#register
	HELP = "-help"
	
	@staticmethod
	def RELATIVE():
		return Set([Keys.CURRENT_WEEK, Keys.PREVIOUS_WEEK, Keys.NEXT_WEEK])
	
	@staticmethod
	def HELP_STRING():
		return "\n\n[{0}] key is start date. ({0} 2016-09-12)\n"\
				  "\tBy default start date is a current date\n"\
				  "\tIf no [{1}] key is entered than report will be filled for one day\n\n"\
				  "[{1}] key is second date. ({1} 2016-09-16)\n"\
				  "\tIf [{0}] key is not entered start date equals to the current date\n\n"\
				  "[{2} {3} {4}]  means current, previous and next week.\n"\
				  "\tCan be combined. But illegal with [{0}] and [{1}] keys\n\n"\
				  "[{5}] key is week number. ({5} 41)'\n"\
				  "\tCan be combined with [{2} {3} {4}] but not with [{0}] and [{1}]\n\n"\
				  "[{6}] key must be followed by profile name or path. ({6} usual day)\n"\
				  "\t [{6}] is a mandatory parameter. If you miss it - error occurs\n\n"\
				  "[{7}] key means that report will be registered instead of store as private\n"\
				  "\tBe accurate with this key as it gives you no possibility to check correctness of inserted data\n\n"\
				  "EXAMPLE: fill_wtr.sh {0} 2016-09-12 {1} 2016-09-16 {6} profile_usual_day.py".format(Keys.START_DAY, Keys.END_DAY, 
				  																					Keys.CURRENT_WEEK, Keys.PREVIOUS_WEEK, Keys.NEXT_WEEK,
				  																					Keys.WEEK, Keys.PROFILE, Keys.EXECUTE)

class State:
	NONE = 0
	DATES = 1#start or end date entered#
	WEEKS = 2#-c, -p or -n key entered#
	ONE_DATE = 3
	OK = 4
	ALREADY_REGISTERED = 5
	ERROR = 6

def addWeek(week):
	weekName = '%d-W%d' % (currentDate.year, week)
	Weeks.append(weekName)
	
def dateMatch(date):
	if re.match("^201\d-[01]\d-[0123]\d$", date):
   		return True
	else:
		return False
		
def weekMatch(week):
	if re.match("\d{2}", week):
		return True
	else:
		return False
	
def parseArgs(args):#return State
	global wtr_date
	global wtr_secondDate
	global wtr_profile
	global currentDate
	global kyeSet
	global ERROR
	
	state = State.NONE
	current_week = currentDate.isocalendar()[1]
	profileFound = False
	
	i = 0
	while i < len(args):
		arg = args[i]
		if arg == Keys.START_DAY:#Begin date
			if state == State.WEEKS:
				state = State.ERROR
				ERROR = "ERROR: both keys {1} and dates entered" % (Keys.RELATIVE())
				break
			
			if dateMatch(args[i + 1]):
				wtr_date = args[i + 1]
				i += 1
			else:
				state = State.ERROR
				ERROR = "ERROR: -start and -end must me followed by date"
				break
				
			keySet.add(arg)
			state = State.DATES
			
		elif arg == Keys.END_DAY:#End date
			if state == State.WEEKS:
				state = State.ERROR
				ERROR = "ERROR: botr keys[-c | -p | -n] and dates entered"
				break
			
			if dateMatch(args[i + 1]):
				wtr_secondDate = args[i + 1]
				i += 1
			else: 
				state = State.ERROR
				ERROR = "ERROR: -start and -end must me followed by date"
				break
			keySet.add(arg)
			state = State.DATES
			
		elif arg == Keys.PROFILE:
			if profileFound:
				state = State.ERROR
				ERROR = "ERROR: -profile key found twise"
				break

			if i + 1 >= len(args):
				state = State.ERROR
				ERROR = "ERROR: key -profile is not followed by profile name"
				break
			else:
				wtr_profile = findProfile(args[i + 1])
				if wtr_profile == "":
					state = State.ERROR
					ERROR = "ERROR: key -profile is followed by wrong profile name"
				else:
					profileFound = True
			keySet.add(arg)
			i += 1
			
		elif arg in Keys.RELATIVE():#Relative week number(from now)
			if state == State.DATES:
				state = State.ERROR
				ERROR = "ERROR: you can't enter both dates and keys -c, -n or -p"
				break
			
			if arg in keySet:
				state = State.ERROR
				ERROR = "ERROR: twise keys " + arg
				break

			keySet.add(arg)
			state = State.WEEKS
			if arg == Keys.CURRENT_WEEK:
				addWeek(current_week)
			elif arg == Keys.PREVIOUS_WEEK:
				addWeek(current_week - 1)
			elif arg == Keys.NEXT_WEEK:
				addWeek(current_week + 1) 
						
		elif arg == Keys.WEEK:
			if state == State.DATES:
				state = State.ERROR
				ERROR = "ERROR: you can't enter both dates and key " + Keys.WEEK
				break
				
			if weekMatch(args[i + 1]):
				state = State.WEEKS
				keySet.add(Keys.WEEK)
				addWeek(int(args[i + 1]))
				i += 1
			else:
				state = State.ERROR
				ERROR = "ERROR: key {1} must be followed by week(EXAMPLE:{1} 2016-W45)" % Keys.WEEK
				break
				
		elif arg == Keys.EXECUTE:#Confirm instead of store as private
			if arg in keySet:
				state = State.ERROR
				ERROR = "ERROR: twise keys " + arg
				break
			
			global registerDay
			global registerWeek
			registerDay = register_Day
			registerWeek = register_Week
			registerPeriod = register_Period
						
		elif arg == Keys.HELP:
			if not keySet:
				print Keys.HELP_STRING()
				exit()
			else:
				state = State.ERROR
				ERROR = "ERROR: -help not allowed here"
				break
			
		elif dateMatch(arg):
			state = State.ERROR
			ERROR = "ERROR: you must enter key -start or -end befor date"
			break
			#as we do i += 1 when hit -start or -end
			
		else: 
			state = State.ERROR
			ERROR = "ERROR: wrong input: " + arg
			break
			
		i += 1
		
	if state == State.ERROR:
		return state
		
	if not profileFound:
		ERROR = "ERROR: No profile entered"
		return State.ERROR
		
	if state == State.NONE:#fill for today
		return State.ONE_DATE
		
	firstDate = getDate(wtr_date)
	secondDate = getDate(wtr_secondDate)
	
	if state == State.DATES:
		if '-start' in keySet:
			if '-end' in keySet:
				if secondDate == firstDate:#start day = end day => one date
					state = State.ONE_DATE
				elif (firstDate - secondDate).days > 0:
					state = State.ERROR
					ERROR = "ERROR: start date is greater than second"
				#else second date is greater than the first and state stays
				#equal to State.DATES

			else:#only start date entered 
				state = State.ONE_DATE
		elif '-end' in keySet:#start date is today
			if secondDate == firstDate:#the same as -start and -end
					state = State.ONE_DATE
			elif (firstDate - secondDate).days > 0:
				state = State.ERROR
				ERROR = "ERROR: start date is greater than second"
		else:
			state = State.ERROR
			ERROR = "ERROR: unexpected error (state = State.DATES but no dates found)"
	elif state == State.WEEKS:
		weekSet = Keys.RELATIVE()
		weekSet.add(Keys.WEEK)
		if len(keySet.intersection(weekSet)) == 0:
			print weekSet
			state = State.ERROR
			ERROR = "ERROR: unexpected error (state = State.WEEKS but no keys found)"
	
	return state
 
def dateMatch(date):
	if re.match("^201\d-[01]\d-[0123]\d$", date):
   		#print "date ok"
   		return True
	else:
		return False

def include(filename):
	if os.path.exists(filename): 
		execfile(filename)
		return True
	else:
		return False

def setSelectControl(browser, controlId, value):
	valId = -2
	control = browser.form.find_control(controlId, nr = 0)
	for item in control.items:
		for label in item.get_labels():
			if label.text == value:
				valId = item.name
				#print "Found controlId %s with id %s" % (label.text, valId)
				control.value = [valId]
				break

	return valId;

def login(browser,url,name,psw):
	browser.open(url)
	browser.form = list(browser.forms())[0]  # use when form is unnamed
	control = browser.form.find_control("UserName")
	control.value = name
	control = browser.form.find_control("Password")
	control.value = psw
	return browser.submit();

def loginPL(browser,url,name,psw):
	browser.open(url)
	browser.form = list(browser.forms())[0]  # use when form is unnamed
	control = browser.form.find_control("login")
	control.value = name
	control = browser.form.find_control("password")
	control.value = psw
	return browser.submit();

def findProfile(profile):#if profile with name in 'sys.argv[argNum]' exists,
						#set wtr_profile to profile's full path and return True
						#else return False
	
	if not re.match("^.*\.py$", profile):
		profile += '.py'
		print profile
	
	if os.path.exists(profile):
		return profile
		
	profile = os.path.basename(profile)
	dirName = os.path.abspath(sys.argv[0])
	profPath = dirName
	prevLen = 0
	
	while len(dirName) != prevLen:
		prevLen = len(dirName)
		dirName = os.path.dirname(dirName)
		profPath = os.path.join(dirName, os.path.join('profiles', profile))#Searching for the profile in dir profiles
		if os.path.exists(profPath):
			return profPath
		else:
			profPath = os.path.join(dirName, profile)#Else in the upper dir
			if os.path.exists(profPath):
				return profPath
				
	
	return ""
	
def createTask(browser, task):
	
	levelList = "taskLevelList[{0}]."
	level = 0
	levelZeroCleared = False
	newReport = browser.form["newWeeklyReport"] #'true' if report is newly created
	
	while True:
		try:
			control = browser.form.find_control((levelList + "taskId").format(level), nr = 0)
			projectControl = browser.form.find_control((levelList + "projectId").format(level), nr = 1)
			if projectControl.value == "-1" or newReport == "true":
				if level == 0:
					if not clearTask(browser, level):
						exit("Couldn't clearTask")
					levelZeroCleared = True	
					
				else:
					removeTask(browser, level)
					level -= 1
		except:
			break
		level += 1
	
	if levelZeroCleared:
		return 0
	else:
		addTask(browser, level)
		
		return level

def removeTask(browser, task):

	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '10'
	
	control = browser.form.find_control("task")
	control.readonly = False
	browser.form['task'] = str(task)
	
	browser.submit()
	
	browser.select_form(name = "editWeeklyReportForm")
	
def clearTask(browser, task):
	
	field = "taskLevelList[%d]." % (task)
	field += "daysDetails[{0}].dailyHoursList[0]."
	
	try:
		for dayInd in range(0, 7):
			current = field.format(dayInd)
			factorId = browser.form.find_control(current + "factorId", nr = 0)
			
			if factorId.value != "-1":# and factorId.value != "107":#107 - Day off
				
				wtr_factor_id = setSelectControl(browser, current.format(dayInd) + "factorId", "none")
				if wtr_factor_id == -2:
					exit("factor not found")
				
				factorId_old = browser.form.find_control(current + "factorId_old", nr = 0)
				factorId_old.readonly = False
				factorId_old.value = "-1"
				
				browser.form[current.format(dayInd) + "hours"] = "0.0"
		
				control = browser.form.find_control(current + "workUnits", nr = 0)
				control.readonly = False				
				browser.form[current.format(dayInd) + "workUnits"] = "0.0"

				browser.form[current.format(dayInd) + "comment"] = ""
				
	except Exception, e:
		#print "EXCEPTION(clearTask): ", str(e)
		return False
		
	return True
	
def addTask(browser, level):
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'

	control = browser.form.find_control("task")
	control.readonly = False
	browser.form['task'] = str(level)
	browser.submit()
	
	browser.form = list(browser.forms())[0]	
	clearTask(browser, level)

def loadProject(browser, idx, level):
	
	if(wtr_project == 'none'):
		wtr_feature = "none"
		wtr_task = "none"
		wtr_dettask = "none"
	else:
		control = browser.form.find_control("act")
		control.readonly = False
		browser.form['act'] = '3'
		
		control = browser.form.find_control(idx)
		control.readonly = False
		browser.form[idx] = str(level)
		
		browser.submit()

def loadTask(browser, idx, level):
	
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '11'
		
	control = browser.form.find_control(idx)
	control.readonly = False
	browser.form[idx] = str(level)
		
	browser.submit()
	
def formChanged(browser):
	control = browser.form.find_control("formChanged")
	control.readonly = False
	browser.form['formChanged'] = 'true'
	
def isDayOff(dayNumber):#saturday and sunday
	if dayNumber >= 6:
		return True
	else: return False
	
###Fill form
def fillOneDayForm(browser):
	browser.select_form(name="editDailyReportForm")

	wtr_location_id = setSelectControl(browser, 'reportUnits[0].locationId', wtr_location)
	if wtr_location_id == -2:
		exit("Location not found")

	wtr_project_id = setSelectControl(browser,'reportUnits[0].projectId',wtr_project)
	if wtr_project_id == -2:
		exit("Project not found")
	else:
		loadProject(browser, 'row', 0)
		browser.select_form(name="editDailyReportForm")

	wtr_feature_id = setSelectControl(browser,'reportUnits[0].featureId',wtr_feature)
	if wtr_feature_id == -2:
		exit("feature not found")

	wtr_task_id = setSelectControl(browser,'reportUnits[0].taskId',wtr_task)
	if wtr_task_id == -2:
		exit("task not found")
	else:	
		loadTask(browser, 'row', 0)
		browser.select_form(name="editDailyReportForm")

	wtr_dettask_id = setSelectControl(browser,'reportUnits[0].taskId',wtr_dettask)
	if wtr_dettask_id == -2:
		exit("dettask not found")

	browser.form['reportUnits[0].hours'] = wtr_hours
	control = browser.form.find_control("reportUnits[0].workUnits")
	control.readonly = False
	browser.form['reportUnits[0].workUnits'] = wtr_units

	wtr_factor_id = setSelectControl(browser,'reportUnits[0].factorId',wtr_factor)
	if wtr_factor_id == -2:
		exit("factor not found")

	browser.form['reportUnits[0].comment'] = wtr_comment

#week form
def fillFewDayReport(browser, firstReportDay, lastReportDay):

	browser.select_form(name = "editWeeklyReportForm")

	level = createTask(browser, wtr_task)
	field = "taskLevelList[%d]." % (level)
	
	#print firstReportDay ," : ", lastReportDay, "\n"
	
	dif = dateDif(firstReportDay, lastReportDay)
	dayNumber = firstReportDay.isocalendar()[2] - 1#numeration from 0
	
	browser.form = list(browser.forms())[0]
	browser.set_all_readonly(False)
	
	wtr_location_id = setSelectControl(browser, field + "locationId", wtr_location)
	if wtr_location_id == -2:
		exit("Location not found")

	wtr_project_id = setSelectControl(browser, field + "projectId", wtr_project)
	if wtr_project_id == -2:
		exit("Project not found")
	else:
		loadProject(browser, 'task', level)
		browser.select_form(name = "editWeeklyReportForm")

	wtr_feature_id = setSelectControl(browser, field + "featureId", wtr_feature)
	if wtr_feature_id == -2:
		exit("feature not found")

	wtr_task_id = setSelectControl(browser, field + "taskId", wtr_task)
	if wtr_task_id == -2:
		exit("task not found")
	else:
		loadTask(browser, 'task', level)
		browser.select_form(name = "editWeeklyReportForm")

	wtr_dettask_id = setSelectControl(browser, field + "detailedTaskId", wtr_dettask)
	if wtr_dettask_id == -2:
		exit("detailed task not found")
			
	field += "daysDetails[{0}].dailyHoursList[0]."
	
	dayOffs = 0
	while dif != 0:
		if (isDayOff(dayNumber + 1) and AutoDayOFF):#needs to be filled in another task
			#print "it is a day off: ", dayNumber + 1, "\n"
			dayOffs += 1
		else:
			try:
				hoursCtrl = browser.form.find_control(field.format(dayNumber) + "hours")
				hoursCtrl.readonly = False
				browser.form[field.format(dayNumber) + "hours"] = wtr_hours
		
				unitsCtrl = browser.form.find_control(field.format(dayNumber) + "workUnits")
				unitsCtrl.readonly = False
				browser.form[field.format(dayNumber) + "workUnits"] = wtr_units

				wtr_factor_id = setSelectControl(browser, field.format(dayNumber) + "factorId", wtr_factor)
				if wtr_factor_id == -2:
					exit("factor not found")

				browser.form[field.format(dayNumber) + "comment"] = wtr_comment
				#print "it is a usual day:", dayNumber + 1, "\n"
				
			except Exception, e:
				#print "day ", dayNumber + 1," is registered", firstReportDay + timedelta(days = dayNumber)
				repStated = "dailyReportStateIdList[%d].value" % (dayNumber + 1) if dayNumber < 6 else 0
				ctrl = browser.form.find_control(repStated)
				if ctrl.value == '1':
					exit("Error: " + str(firstReportDay + timedelta(days = dayNumber)) + " is registered.\nYou must fill this week by your self\n")
				exit(str(e))
					
				
		dayNumber += 1
		dif -= 1
		
	if AutoDayOFF and dayOffs:
		level += 1
		addTask(browser, level)
		field = "taskLevelList[%d]." % (level)
		field += "daysDetails[{0}].dailyHoursList[0]."
		
		dayNumber = 5 #6th day of week
		while dayOffs > 0:
			#print "fill a day off: ", dayNumber + 1, "\n"
			#try:
			hoursCtrl = browser.form.find_control(field.format(dayNumber) + "hours")
			hoursCtrl.readonly = False
			browser.form[field.format(dayNumber) + "hours"] = "0"
		
			unitsCtrl = browser.form.find_control(field.format(dayNumber) + "workUnits")
			unitsCtrl.readonly = False
			browser.form[field.format(dayNumber) + "workUnits"] = "0"

			factor = browser.form.find_control(field.format(dayNumber) + "factorId")		
			
			wtr_factor_id = setSelectControl(browser, field.format(dayNumber) + "factorId", wtr_dayOffFactor)
			if wtr_factor_id == -2:
				exit("factor not found")
				
			factor_old = browser.form.find_control(field.format(dayNumber) + "factorId_old")
			factor_old.readonly = False
			factor_old.value = factor.value[0]
				

			browser.form[field.format(dayNumber) + "comment"] = ""
			#except:#this day is registered
				#print dayNumber + 1," is registered"
				#go to the next day
		
			dayNumber += 1
			dayOffs -= 1
			
		
			
###----------------------------------

###Register day
def storeAsPrivate_Day(browser):
	fillOneDayForm(browser)

	return submitDayForm(browser, '5')

def register_Day(browser):
	fillOneDayForm(browser)

	return submitDayForm(browser, '6')
###-------------------

def getFirstDay(week):
	return datetime.strptime(week + '-1', "%Y-W%W-%w").date()
	
def getLastDay(week):
	return datetime.strptime(week + '-0', "%Y-W%W-%w").date()

def submitDayForm(browser, action):
	if not action in ['6','5']:
		ERROR = "ERROR: wrong action"
		return False
	else:
		control = browser.form.find_control("act")
		control.readonly = False
		browser.form['act'] = action

		response = browser.submit()
		return True
		
###Register few days
def storeAsPrivate_Period(browser, firstDay, lastDay):
		
	fillFewDayReport(browser, firstDay, lastDay)
	
	submitWeekForm(browser, '4')

def register_Period(browser, firstDay, lastDay):
		
	fillFewDayReport(browser, firstDay, lastDay)	
	
	submitWeekForm(browser, '5')
	
def	register_Week(browser, week):
	
	firstDay = getFirstDay(week)
	lastDay = getLastDay(week)
	
	fillFewDayReport(browser, firstDay, lastDay)	
	
	submitWeekForm(browser, '5')
	
def storeAsPrivate_Week(browser, week):
	firstDay = getFirstDay(week)
	lastDay = getLastDay(week)
		
	fillFewDayReport(browser, firstDay, lastDay)
	
	submitWeekForm(browser, '4')

	
def submitWeekForm(browser, action):
	if not action in ['4','5']:
		ERROR = "ERROR: wrong action"
		return False
	else:
		control = browser.form.find_control("act")
		control.readonly = False
		browser.form['act'] = action
		response = browser.submit()
		return True
		
###-------------------------------		
def getWeek(someDate):
	return someDate.isocalendar()[1]
	
###Open day form
def openDayForm(browser, page):
	global ERROR
	global state
	
	browser.open(page)
	browser.select_form(name="myWeekReportsForm")
	browser.form['editDayDate'] = wtr_date
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'
	browser.submit()

	browser.form = list(browser.forms())[0]
	
	if browser.title() != "Edit Daily Report":
		exit('Unable to open "Edit Daily Report" page')
	elif browser.form['state'] != 'REGISTERED':
		return True
	else:
		ERROR = wtr_date + " is already registered"
		state = State.ALREADY_REGISTERED
		return False
###--------------------------

###Open week form
def openFewDaysForm(browser, page, firstDay, lastDay):
	dif = dateDif(firstDay, lastDay)

	weekDay = firstDay.isocalendar()[2]

	if (dif + weekDay - 1) > 7:
		exit("ERROR: wrong dates(corrupts two weeks)")
	elif dif <= 0:
		exit("ERROR: start date is greater than end date")
	
	week = getWeek(firstDay)

	wtr_week = "%d-W%d" % (firstDay.year, week)

	return openWeekForm(browser, page, wtr_week)

def openWeekForm(browser, page, week):
	global ERROR
	global state	
	
	browser.open(page)
	browser.select_form(name = "myWeekReportsForm")
	browser.form['editWeekDate'] = week

	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '7'
	
	control = browser.form.find_control("weekDetails")
	control.readonly = False
	browser.form['weekDetails'] = week

	browser.submit()
	
	browser.form = list(browser.forms())[0];
	
	if browser.title() != "Edit weekly report":
		exit('Unable to open "Edit weekly report" page')
	elif browser.form["toRegister"] == 'true':
		return True
	else:
		ERROR = week + " is already registered"
		state = State.ALREADY_REGISTERED
		return False
	
###------------------------------
	
def confirm(browser):
	global state	
	
	if state == State.ALREADY_REGISTERED:
		return
	
	if browser.title() != "Confirmation page":
		exit("Confirm failed")
	
	browser.select_form(name = "confirmationStorRegDailyReportForm")
	
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'# confirm
	
	response = browser.submit()	

def dateDif(first, second):
	return (second-first).days + 1

def getDate(date):
	return datetime.strptime(date, "%Y-%m-%d").date()

def differentWeeks(firstDate, secondDate):
	if firstDate.isocalendar()[1] != secondDate.isocalendar()[1]:
		return True
	else: return False

def lastDayOfWeek(someDate):
	diff = 7 - someDate.isocalendar()[2]
	return someDate + timedelta(days = diff)

#### default values
#should be overwritten by profile
wtr_location = "EPBY/BR/D"
wtr_project = "EPBY TC2 Internal not billable hours [3677]"
wtr_feature = "none"
wtr_task = "none"
wtr_dettask = "none"
wtr_hours = "8"
wtr_units = "0"
wtr_factor = "Standard"
wtr_comment = ""
#
wtr_dayOffFactor = "Day Off"
#
currentDate = datetime.now()
wtr_date = currentDate.strftime("%Y-%m-%d")#initialize it with todays date
wtr_secondDate = currentDate.strftime("%Y-%m-%d")#initialize it with todays date
wtr_week = '%d-W%d' % (currentDate.year, currentDate.isocalendar()[1])#initialize it with current year and week
wtr_profile = ""
Weeks = []
keySet = Set()
ERROR = ""
AutoDayOFF = True

registerDay = storeAsPrivate_Day
registerWeek = storeAsPrivate_Week
registerPeriod = storeAsPrivate_Period
   
if(include(os.path.join(os.path.dirname(sys.argv[0]), "login.py")) == False):
	exit("ERROR: No login and password(file 'login.py' must be in the same directory))")#login and password

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11')]

brPL = mechanize.Browser()
brPL.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11')]
###### LOGIN ########

login(br,"https://websession-wcf.office.int/?ReturnUrl=http://wtr-epby.office.int/worktimereport/myweekreports.do#", wtr_login, wtr_password)

strTitle = br.title()
if strTitle != "My weekly reports":
	exit("Login failed")

# for PL version
loginPL(brPL,"http://epol.ericpol.int:8080/websession/login?redir=http://wtr.ericpol.int:8080/worktimereport/", wtr_login, wtr_password)

strTitle = brPL.title()
if strTitle != "My weekly reports":
	exit("LoginPL failed")

state = parseArgs(sys.argv[1:])
if state == State.ERROR:
	exit(ERROR)
	
elif state == State.ONE_DATE:
	if include(wtr_profile) == False:
		exit("ERROR: Unable to include profile")
		
	print "one day report: ", wtr_date
	
	if openDayForm(br,"http://wtr-epby.office.int/worktimereport/"):
		registerDay(br)
	else:
		print ERROR

	if openDayForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/myweekreports.do"):
		registerDay(brPL)
	else:
		print ERROR
	
	confirm(br)
	confirm(brPL)
	state = State.OK

elif state == State.DATES:
	print "Filling report for period: {0} - {1}".format(wtr_date, wtr_secondDate)
	if include(wtr_profile) == False:
		exit("ERROR: Unable to include profile")
	
	firstDate = getDate(wtr_date)
	secondDate = getDate(wtr_secondDate)
	
	while differentWeeks(firstDate, secondDate):#firstDate and secondDate are on different weeks
		nextDate = lastDayOfWeek(firstDate)
		if openFewDaysForm(br,"http://wtr-epby.office.int/worktimereport/", firstDate, nextDate):
			registerPeriod(br, firstDate, nextDate)
		else:
			print ERROR

		if openFewDaysForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/index.do", firstDate, nextDate):
			registerPeriod(brPL, firstDate, nextDate)
		else:
			print ERROR
		confirm(br)
		confirm(brPL)
		state = State.OK
		firstDate = nextDate + timedelta(days = 1)
	else:
		if firstDate <= secondDate:
			print firstDate, "   ", secondDate
			if openFewDaysForm(br,"http://wtr-epby.office.int/worktimereport/", firstDate, secondDate):
				registerPeriod(br, firstDate, secondDate)
			else:
				print ERROR

			if openFewDaysForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/index.do", firstDate, secondDate):
				registerPeriod(brPL, firstDate, secondDate)
			else:
				print ERROR

			confirm(br)
			confirm(brPL)	
			state = State.OK
elif state == State.WEEKS:
	print "Filling report for weeks: ", Weeks
	if include(wtr_profile) == False:
		exit("EXIT: Unable to include profile")

	for week in Weeks:
		#print "wtr.by\n....."
		if openWeekForm(br,"http://wtr-epby.office.int/worktimereport/", week):
			registerWeek(br, week)
		elif state == State.ERROR:
			exit(ERROR)
		else:
			print ERROR
		#print "wtr.by done"

		#print "wtr.pl\n....."
		if openWeekForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/index.do", week):
			registerWeek(brPL, week)
		elif state == State.ERROR:
			exit(ERROR)
		else:
			print ERROR
		#print "wtr.pl done"
		
		confirm(br)
		confirm(brPL)
		state = State.OK

exit("All done")
##############
