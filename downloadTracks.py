from lxml import etree
import urllib2
import re
import sys
import subprocess

argList = sys.argv
print "The URL is " + str(argList[1])
print "Directory to save files to is " + str(argList[2])
# send request to the url of the smagam
smagamUrl=argList[1]
directory=argList[2]
f = urllib2.urlopen(smagamUrl)
tree = etree.HTML(f.read())
heading = tree.xpath("//tr/td[@class='Header']")
city,smagam,month,year = heading[0].text.split()
sections = tree.xpath("//table/tr[@class='whaitenack']/parent::node()")
dictionary = dict()
for i in range(1, len(sections)):
	if i > 0:
		s = sections[i]
		# iterate through all of the "tr"
		table_rows = s.xpath("tr")
		track_list = []
		for z in range(0,len(table_rows)):
			tr = table_rows[z]
			if z == 0:
				title = tr.xpath("td/font[@class='title']")[0].text
			else:
				# get all the other data
				# second column = name
				# fourth column = url
				td = tr.xpath("td")
				result = []
				if len(td) > 1:
					keertanee_name = td[1].text.encode('utf-8')
					keertanee_name = keertanee_name.replace('\xc2\xa0','')
					url = td[3].xpath("a")[0].attrib['href']
					result.append(keertanee_name)
					result.append(url)
					track_list.append(result)

		dictionary[title]=track_list

for title in dictionary:
	tracks = dictionary[title]
	for t in tracks:
		keertanee = t[0]
		url = t[1]
		# create new file name
		# get the number from the url
		num = re.search('http://www(.*)/'+year+'\d+\D+(.*?)\D+(.*)$',url)
		new_num =  num.group(2)
		#track_title = str(new_num) + " " +  str(city) + " " + str(month) + " " +  str(year) + " " +  keertanee + ".mp3"
		track_title = str(new_num) + " " +  str(city) + " " + str(month) + " " +  str(year) + " " +  keertanee + ".mp3"
		print track_title
		re.escape(track_title)
		command = 'curl ' + url + ' -o \"' + directory + track_title + "\""
		print command
		# move from os.system to sub process call
		#os.system(command)
		#status = subprocess.call(['curl',url,'-o','\"' + directory + track_title + '\"'])
		status = subprocess.call(['curl',url,'-o',directory + track_title])
		if status == 0:
			print "Track downloaded successfully"
		else:
			print "Track did not download succesfully"
			print "status code = " + str(status)
		#os.system('curl ' + url + '-o \"' + track_tile + "\"")




