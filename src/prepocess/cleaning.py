import json
import os
import re
import regex
import sys
import emoji
import ntpath

stopwords = {}
positive_word = {}
negative_word = {}


def extractEmojis(text):
	emoji_list = []
	data = regex.findall(r'\X', text)
	for word in data:
		if any(char in emoji.UNICODE_EMOJI for char in word):
			emoji_list.append(word)
	return emoji_list


def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)


def readFile(pathFile):
	return os.popen('cat ' + str(pathFile)).read()


def getAllFilesInPath(pathFolder):
	return ["{}{}".format(pathFolder + '/', i) for i in os.popen('ls ' + str(pathFolder)).read().split('\n')]


def findall(search, txt):
	return re.findall(search, txt)


def search(search, txt):
	return re.search(search, txt)


def replace(search, rep, txt):
	return re.sub(search, rep, txt)


def cleanText(txt):
	txt = replace(">", ' ', txt)
	txt = txt.replace('\\n', ' ')
	txt = txt.replace('\t', ' ')
	txt = txt.replace('\\', ' ')
	txt = replace("&(.*?)", ' ', txt)
	txt = replace("[\s,\n,'']&(.*?)", ' ', txt)
	txt = replace("[\:\]\|\[\@\$\%\*\&\/\(\)\;\"]+ ", ' ', txt)
	txt = replace("\n+", ' ', txt)
	txt = replace("^\s+", ' ', txt)
	txt = replace("\s+$", ' ', txt)
	txt = replace("^$", '', txt)
	txt = replace("\!", ' ', txt)
	txt = replace("\*", ' ', txt)
	txt = replace("\.+ ", '', txt)
	txt = replace("\w\,", ' ', txt)
	txt = replace("\s+", ' ', txt)
	txt = replace("^\s+|\s+$", ' ', txt)
	return txt


def clean_format(txt):
	txt = replace("http://[^ ]*", ' ', txt)
	txt = replace("https://[^ ]*", ' ', txt)
	return txt


def initFile(stopwordF, positiveF, negativeF):
	global stopwords
	global positive_word
	global negative_word

	data = readFile(stopwordF).split('\n')
	for term in data:
		stopwords[term] = 1

	data = readFile(positiveF).split('\n')
	for term in data:
		positive_word[term] = 1

	data = readFile(negativeF).split('\n')
	for term in data:
		negative_word[term] = 1


def isset(variable):
	return variable in locals() or variable in globals()


def getTweet(text):
	return text


def getTag(text):
	return text


def getEmoticon(text):
	return text


def makeData(text, hashtags, mention, emoji, date, time):
	return json.dumps({
		"text": text,
		"hashtags": hashtags,
		"mention": mention,
		"emoji": emoji,
		"date": date,
		"time": time
	})


def saveFile(data_text, dst):
	file = open(dst, "w+")
	for text in data_text:
		file.write(json.dumps(text) + "\n")
	file.close()


def arrayToString(separator, arr):
	return separator.join(arr)


def cleanFiles(path,dst):

	cntr = 0
	files = getAllFilesInPath(path)
	lenFiles = len(files) - 1

	for file in files:
		if (ntpath.basename(file) == ''):
			continue
		clean_file = {
			"name": file,
			"file": []
		}

		for line in readFile(file).split('\n'):
			if len(line) < 3:
				continue
			text = findall('"tweet": "(.*?)"', line)
			if len(text) == 0:
				continue

			hashtags = findall('"hashtags": \["(.*?)"\]', line)
			mention = findall('"mentions": \["(.*?)"\]', line)
			date = findall('"date": \["(.*?)"\]', line)
			time = findall('"time": \["(.*?)"\]', line)
			text = cleanText(clean_format(text[0]))
			emoji = extractEmojis(line)
			formatData = makeData(text, hashtags, mention, emoji, date, time)
			clean_file['file'] += [formatData]

		print("done :", cntr, "from", lenFiles)
		cntr += 1
		writeFiles(clean_file, dst)


def writeFiles(file, path):
	print("Start Save Files")
	counter = 0

	if ntpath.basename(file['name']) == '':
		return
	saveFile(file['file'], path + ntpath.basename(file['name']))
	counter += 1


def main():
	counter = 1
	cmd = {}

	# for get cmd with -flag
	for cmdLine in sys.argv[1:]:
		if (cmdLine[:1] == '-' and counter + 1 < len(sys.argv)):
			cmd[cmdLine] = sys.argv[counter + 1]
		counter += 1

	cleanFiles(cmd['-src'],cmd['-dst'])

# argv -src path-data -dst path-dst
main()
