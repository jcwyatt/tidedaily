#A python program to import tide data from a gov.je website
#tidescrape5.0.py - working fine
#It pulls the data in from the gov.je tide site, wkhich is updated daily
#It looks for the class headers associated with date,time and height information
#and then creates a list of these bits of html

#this version(6.0) is called by a chrontab function and tweets at 5:30am everyday.

import tweepy
import smtplib
import urllib2
import re
from bs4 import BeautifulSoup
from time import sleep
import datetime as dt



#function to scrape tide data from website
def tidedatascrape():

	#open site
	rawhtml = urllib2.urlopen("http://www.gov.je/Weather/Pages/Tides.aspx").read(20000)

	soup = BeautifulSoup(rawhtml)

	#below learnt from http://stackoverflow.com/questions/14257717/python-beautifulsoup-wildcard-attribute-id-search

	#get the dates:
	tidedates = soup.findAll('td', {'class': re.compile('TidesDate.*')} )
	#get the times:
	tidetimes = soup.findAll('td', {'class': re.compile('TidesTime.*')} )
	#get the heights:
	tideheights = soup.findAll('td', {'class': re.compile('TidesHeight.*')} )

	#collect together the data for today

	todaysdate = tidedates[0].get_text()
	print (todaysdate)
	todaystimes = tidetimes[0].get_text()
	print (todaystimes)
	todaysheights = tideheights[0].get_text()
	print (todaysheights)


	#parse the times (always a 5 character string)
	ttime = [0,0,0,0]
	for i in range (0,4):
		ttime[i]=todaystimes[5*i:(5*i+5)]
		print ttime[i]


	#parse the heights (3 or 4 ch string delimited by 'm' e.g 2.5m3.4m etc)
	theight = ['','','','']
	list_index = 0
	for i in todaysheights:
		if i == 'm':
			list_index += 1
		else:
			theight[list_index] = theight[list_index] + i
	print theight[0]



	#create a tweetable string of all the data
	tweetstring = ('#tides for #jerseyci today, ' + todaysdate + ':\n')
	for i in range (0,4):
		tweetstring = tweetstring + (ttime[i] + ' ' + theight[i] + 'm\n')
	tweetstring = tweetstring + 'data from http://mbcurl.me/13KDW'
	print tweetstring
	return tweetstring
	

	#print len(tweetstring) #just to check it is within 140 characters

#function to write to a text file for webpage or other use.
def writetidestofile(tweetstring):
        with open('/var/www/dailytideoutput.txt','w') as f:
                f.write(str(tweetstring))
                f.close()


#function to tweet it
def tweettidedata(tweetstring):
	CONSUMER_KEY = 'KEY'#keep the quotes, replace this with your consumer key
	CONSUMER_SECRET = 'SECRET'#keep the quotes, replace this with your consumer secret key
	ACCESS_KEY = 'A_KEY'#keep the quotes, replace this with your access token
	ACCESS_SECRET = 'A_SECRET'#keep the quotes, replace this with your access token secret
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

#	api.update_status(status="This is Jason's Pi. I'm a bit bored of tweeting tides. I'll still be posting tide times each day @ http://jcwyatt.ddns.net" ) #THIS LINE TWEETS! - LEAVE DEACTIVATED UNTIL READY


#email it(commented out for now)
'''fromaddr = 'f.bloggs@gmail.com' #insert your own from address
toaddr  = 'j.puddleduck@holier.sch.uk' #insert your own to address

# Credentials (if needed)
username = raw_input('gmail un: ')
password = raw_input('gmail pw: ')

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587') #insert your own SMTP server details
server.ehlo()
server.starttls()
server.login(username,password)
headers = "\r\n".join(["from: " + fromaddr,
                       "subject: " + 'Tides Today',
                       "to: " + toaddr,
                       "mime-version: 1.0",
                       "content-type: text/html"])

# body_of_email can be plaintext or html                    
content = headers + "\r\n\r\n" + tweetstring
server.sendmail(fromaddr, toaddr, content)
server.quit
'''

#main prog
#collect data
tweetstring = tidedatascrape()
#output to file
writetidestofile(tweetstring)
#tweet data
tweettidedata(tweetstring)	

