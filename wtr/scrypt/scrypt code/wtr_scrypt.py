#!/usr/bin/python
import re
import mechanize
import sys
import os.path
import webbrowser

from datetime import date
from datetime import datetime
from datetime import timedelta


wtr_login = ""#in file login.py
wtr_password = ""
 
def dateMatch(date):
	if re.match("^201\d-[01]\d-[0123]\d$", date):
   		print "date ok"
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
    
'''def setSelectForWeekly(browser, controlId, value):#!!not finished
	valId = -2
	control = browser.form.find_control(name = controlId, nr = 0)
	#print("searching for: ", controlId)
	for control in browser.form.controls:
		if control.name == controlId and control.type == "select":
			#print("found: ", control.name)
			for item in control.items:
				for label in item.get_labels():
					#print("\tvalues: ", label)
					if label.text == value:
						valId = item.name
						#print "Found controlId %s with id %s" % (label.text, valId)
						browser.form[controlId] = [valId]
						break
		break
		
	return valId;'''

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

def parseArgs(nextArg):
	if len(sys.argv) < (nextArg + 1):
		raise "ERROR: lack of arguments"

	if dateMatch(sys.argv[nextArg]):
		if dateMatch(sys.argv[nextArg + 1]):
			if len(sys.argv) < (nextArg + 2):
				exit("ERROR: lack of arguments(no profile path)")
			elif os.path.exists(sys.argv[nextArg + 2]):
				return "period"
			else:
				exit("ERROR: wrong profile path in argument number {0}".format(nextArg + 1))
		elif os.path.exists(sys.argv[nextArg + 1]):
			return "one day"
	else:
		exit("ERROR: in argument number {0}".format(nextArg - 1))

def createTask(browser, task):
	
	levelList = "taskLevelList[{0}]."
	level = 0
	
	while True:
		try:
			control = browser.form.find_control((levelList + "taskId").format(level), nr = 0)
			projectControl = browser.form.find_control((levelList + "projectId").format(level), nr = 1)
			if projectControl.value == "-1":
				if level == 0:
					clearTask(browser, level)
				else:
					removeTask(browser, level)
					level -= 1
		except:
			break
			
		level += 1
		
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'
	
	control = browser.form.find_control("task")
	control.readonly = False
	browser.form['task'] = str(level)
	
	browser.submit()
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
			control = browser.form.find_control(current + "factorId", nr = 0)
			
			if control.value != "-1":
				wtr_factor_id = setSelectControl(browser, current.format(dayInd) + "factorId", "none")
				if wtr_factor_id == -2:
					exit("factor not found")
				
				browser.form[current.format(dayInd) + "hours"] = "0.0"
		
				control = browser.form.find_control(current + "workUnits", nr = 0)
				control.readonly = False				
				browser.form[current.format(dayInd) + "workUnits"] = "0.0"

				browser.form[current.format(dayInd) + "comment"] = ""
				
	except Exception, e:
		print str(e)

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


def fillOneDayForm(browser):
	browser.select_form(name="editDailyReportForm")

	wtr_location_id = setSelectControl(browser,'reportUnits[0].locationId',wtr_location)
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

def fillFewDayReport(browser):

	browser.select_form(name = "editWeeklyReportForm")

	level = createTask(browser, wtr_task)
	field = "taskLevelList[%d]." % (level)
	
	firstReportDay = getDate(wtr_date)
	lastReportDay = getDate(wtr_secondDate)
	
	firstDayOfWeek = firstReportDay - timedelta(days = (firstReportDay.isocalendar()[2] - 1))
	
	dif = dateDif(firstReportDay, lastReportDay)
	dayNumber = firstReportDay.isocalendar()[2] - 1
	
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
	
	while dif != 0:
		browser.form[field.format(dayNumber) + "hours"] = wtr_hours
		
		browser.form[field.format(dayNumber) + "workUnits"] = wtr_units

		wtr_factor_id = setSelectControl(browser, field.format(dayNumber) + "factorId", wtr_factor)
		if wtr_factor_id == -2:
			exit("factor not found")

		browser.form[field.format(dayNumber) + "comment"] = wtr_comment
		
		dayNumber += 1
		dif -= 1
		print("NEXT DAY------\n\n")
	

def registerOneDayReport(browser):
	fillOneDayForm(browser)

	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '5'# store as private

	response = browser.submit()

def getWeek(someDate):
	return someDate.isocalendar()[1]

def registerFewDayReport(browser, firstDay, lastDay):
		
	fillFewDayReport(browser)	
	
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '4'# store as private

	response = browser.submit()

def openDayForm(browser, page):
	browser.open(page)
	browser.select_form(name="myWeekReportsForm")
	browser.form['editDayDate'] = wtr_date
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'
	browser.submit()

	if browser.title() != "Edit Daily Report":
		exit('Unable to open "Edit Daily Report" page')

def openWeekForm(browser, page, firstDay, lastDay):
	dif = dateDif(firstDay, lastDay)

	if dif > 7:
		exit("Too mutch days")
	elif dif <= 0:
		print "First date is later or equls than second date",
		print "First date changed with the second"
		wtr_date = wtr_secondDate
	
	week = getWeek(firstDay)

	wtr_week = "%d-W%d" % (firstDay.year, week)

	browser.open(page)
	browser.select_form(name = "myWeekReportsForm")
	browser.form['editWeekDate'] = wtr_week

	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '7'
	
	control = browser.form.find_control("weekDetails")
	control.readonly = False
	browser.form['weekDetails'] = wtr_week

	browser.submit()

	if browser.title() != "Edit weekly report":
		exit('Unable to open "Edit weekly report" page')


def storeAsPrivateConfirm(browser):
	if browser.title() != "Confirmation page":
		#print response.read()
		exit("Confirm failed(on store as private)")
	
	browser.select_form(name = "confirmationStorRegDailyReportForm")
	
	control = browser.form.find_control("act")
	control.readonly = False
	browser.form['act'] = '1'# confirm
	
	response = browser.submit()
	webbrowser.open(browser.geturl())	

def dateDif(first, second):
	return (second-first).days + 1

def getDate(date):
	return datetime.strptime(date, "%Y-%m-%d").date()

#try:
#    from BeautifulSoup import BeautifulSoup
#except ImportError:
#    from bs4 import BeautifulSoup

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
wtr_date = '2016-07-28'
wtr_secondDate = '2016-07-29'
wtr_week = '2016-W34'


if len(sys.argv) < 3:
   exit("lack of arguments( < 2)")
   
if(include(os.path.join(os.path.dirname(sys.argv[0]), "login.py")) == False):
	exit("No login and password(file 'login.py'))")#login and password

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


print 'Number of arguments:', len(sys.argv), 'arguments.'
nextArg = 1
while nextArg < len(sys.argv):
	argsType = parseArgs(nextArg)
	if argsType == "one day":
		print "one day report: ", sys.argv[1]
		wtr_date = sys.argv[nextArg]
		if include(sys.argv[nextArg + 1]) == False:
			exit("EXIT: Unable to include profile")
		
		openDayForm(br,"http://wtr-epby.office.int/worktimereport/")
		registerOneDayReport(br)

		openDayForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/myweekreports.do")
		registerOneDayReport(brPL)
		
		storeAsPrivateConfirm(br)
		storeAsPrivateConfirm(brPL)
		
		nextArg = nextArg + 2

	elif argsType == "period":
		print "Filling report for period: {0} - {1}".format(sys.argv[nextArg], sys.argv[nextArg + 1])
		wtr_date = sys.argv[nextArg]
		wtr_secondDate = sys.argv[nextArg + 1]
		if include(sys.argv[nextArg + 2]) == False:
			exit("EXIT: Unable to include profile")
		
		print "wtr.by"
		openWeekForm(br,"http://wtr-epby.office.int/worktimereport/", getDate(wtr_date), getDate(wtr_secondDate))
		registerFewDayReport(br, wtr_date, wtr_secondDate)
		print "wtr.by done"
		#http://wtr.ericpol.int:8080/worktimereport/myweekreports.do
		
		print "wtr.pl"
		openWeekForm(brPL,"http://wtr.ericpol.int:8080/worktimereport/index.do", getDate(wtr_date), getDate(wtr_secondDate))
		registerFewDayReport(brPL, wtr_date, wtr_secondDate)
		print "wtr.pl done"
		
		storeAsPrivateConfirm(br)
		storeAsPrivateConfirm(brPL)

		nextArg = nextArg + 3
		
	print("nextArg = ", nextArg)
	raw_input("Press Enter to continue")

exit("All done")











