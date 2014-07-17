from lxml import etree
import requests
import re
import os
import sys

argList = sys.argv
print "The URL is " + str(argList[1])
print "Directory to save files too is " + str(argList[2])
# send request to the url of the smagam
smagamUrl=argList[1]
directory=argList[2]
r = requests.get(smagamUrl)
#f = open("sample.html", "r")
tree = etree.HTML(r.text)
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
		for z in range(0,len(table_rows)-1):
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
		track_tile = str(new_num) + " " +  str(city) + " " + str(month) + " " +  str(year) + " " +  keertanee + ".mp3"
		print track_tile
		command = 'curl ' + url + ' -o \"' + directory + track_tile + "\""
		print command
		os.system(command)
		#os.system('curl ' + url + '-o \"' + track_tile + "\"")


# title ---> keertanee --> URL
# each title has multiple keertanees
# title is the key in the dictionary
# each title contains a list of lists
# each list in the list has a value at [0,1]


#f.close()



