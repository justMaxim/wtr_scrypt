# wtr_scrypt

how to run

1. Download the latest release. 
2. Download some profile and edit it coresponding to your requirements(wtr/profiles/...).
3. Enter your login and password in file login.py(wtr/scrypt/login.py)!
4. Run bashscrypt(wtr/scrypt/<bashscrypt_name>.sh) in the terminal.
5. Keys:
   [-date] key is start date. (-date 2016-09-12)
	   By default start date is a current date
	   If no [-sec] key is entered than report will be filled for one day

   [-sec] key is second date. (-sec 2016-09-16)
	   If [-date] key is not entered start date equals to the current date

   [-c -p -n]  means current, previous and next week.
	   Can be combined. But illegal with [-date] and [-sec] keys

   [-week] key is week number. (-week 41)'
	   Can be combined with [-c -p -n] but not with [-date] and [-sec]

   [-profile] key must be followed by profile name or path. (-profile usual day)
	   [-profile] is a mandatory parameter. If you miss it - error occurs

   [-register] key means that report will be registered instead of store as private
	   Be accurate with this key as it gives you no possibility to check correctness of inserted data
 6. Examples:
   EXAMPLE 1: bashscrypt.sh -start 2016-09-01 -end 2016-09-03  -profile profile_usual_day.py
   EXAMPLE 2: bashscrypt.sh -c -profile profile_usual_day.py
   EXAMPLE 3: bashscrypt.sh -profile profile_usual_day.py -c -p -n -register
   EXAMPLE 4: bashscrypt.sh -week 45 -p -c -profile profile_usual_day.py

I am not sure if this is more convinient for you but you can at least try.
