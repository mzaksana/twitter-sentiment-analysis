import json
import os
import re
import sys
from collections import OrderedDict
import matplotlib.pyplot as pPlot
from wordcloud import WordCloud, STOPWORDS
import random

import numpy as npy
from PIL import Image

stopwords = {}

positive_word = {}
negative_word = {}

data = {}
best = {}
worst = {}

add_word = {}


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(20, 50)


def orderDesc(data):
	return OrderedDict(sorted(data.items(), key=lambda kv: kv[1]['count'], reverse=True))


def readFile(pathFile):
	return os.popen('cat ' + str(pathFile)).read()


def findall(search, txt):
	return re.findall(search, txt)


def search(search, txt):
	return re.search(search, txt)


def replace(search, rep, txt):
	return re.sub(search, rep, txt)


def is_hashtag(term):
	if term[0] == "#":
		return True


def is_mention(term):
	if term[0] == "@":
		return True


def is_char(term):
	if len(term) <= 2:
		return True


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


def initFile(stopwordF, positiveF, negativeF, addF):
	global stopwords
	global positive_word
	global negative_word
	global add_word

	data = readFile(stopwordF).split('\n')
	for term in data:
		stopwords[term] = 1

	data = readFile(positiveF).split('\n')
	for term in data:
		positive_word[term] = 1

	data = readFile(negativeF).split('\n')
	for term in data:
		negative_word[term] = 1

	data = readFile(addF).split('\n')
	for term in data:
		add_word[term] = 1


def isset(variable):
	return variable in locals() or variable in globals()


def insertData(data):
	global best
	global worst
	global stopwords
	global positive_word
	global negative_word
	global add_word

	if data['Class'] == "positive":
		if data['air-line'] not in best:
			best[data['air-line']] = {}
		skip = []
		for term in cleanText(data['text']).lower().strip().split(" "):
			if term in stopwords or term in add_word or term in skip or is_hashtag(term) or is_mention(term) or is_char(
					term) or term in negative_word:
				continue
			if term not in best[data['air-line']]:
				best[data['air-line']][term] = {'count': 1}
			else:
				best[data['air-line']][term]['count'] += 1
			skip.append(term)

	elif data['Class'] == "negative":
		if data['air-line'] not in worst:
			worst[data['air-line']] = {}
		skip = []
		for term in cleanText(data['text']).lower().strip().split(' '):
			if term in stopwords or term in add_word or term in skip or is_hashtag(term) or is_mention(term) or is_char(
					term) or term in positive_word:
				continue
			if term not in worst[data['air-line']]:
				worst[data['air-line']][term] = {'count': 1}
			else:
				worst[data['air-line']][term]['count'] += 1
			skip.append(term)


def initData(src):
	file = readFile(src).split("\n")
	for line in file:
		if line == '':
			continue
		line_data = json.loads(line)
		if line_data['text'] == '':
			continue
		insertData(line_data)

def create_word_cloud(string,file):
	# maskArray = npy.array(Image.open("cloud.png"))
	# cloud = WordCloud(background_color="white", max_words=200, mask=maskArray)
	cloud = WordCloud(collocations=False, background_color="white", max_words=200)
	cloud.generate(cleanText(string))
	cloud.recolor(color_func=grey_color_func, random_state=3)
	cloud.to_file("img/"+file+".png")


def rankData():
	global best
	global worst
	pos = " "
	neg = " "
	for key in best.keys():
		print("\n\nKey", key)
		air = key
		air_best = orderDesc(best[key])
		air_worst = orderDesc(worst[key])
		keys_best = air_best.keys()
		keys_worst = air_worst.keys()

		top = 25
		count_p = 0
		print("\n Positive")
		# text = " "
		for key in keys_best:
			top -= 1
			print(key, air_best[key])
			pos += " " + ((key+' ') * int(air_best[key]['count']))
			count_p += air_best[key]['count']
			if top == 0:
				break
		top = 25

		print("count", count_p)
		count_n = 0
		print("\n Negative")
		text = " "
		for key in keys_worst:
			top -= 1
			print(key, air_worst[key])
			count_n += air_worst[key]['count']
			neg += " " + ((key+' ') * int(air_worst[key]['count']))

			if top == 0:
				break

		# print("word",cleanText(text.strip()))
		# create_word_cloud(text.strip(), air+'-neg')
		print("count", count_n)
		print("count + ", count_n + count_p)
	create_word_cloud(pos.strip(), 'pos')
	create_word_cloud(neg.strip(), 'neg')



# print("total")
# for key in best.keys():
# 	print("\n\nKey", key,len(best[key]),len(worst[key]))


def main():
	counter = 1
	cmd = {}
	global data
	# for get cmd with -flag
	for cmdLine in sys.argv[1:]:
		if (cmdLine[:1] == '-' and counter + 1 < len(sys.argv)):
			cmd[cmdLine] = sys.argv[counter + 1]
		counter += 1

	initFile(cmd['-stop'], cmd['-positive'], cmd['-negative'], cmd['-add'])
	initData(cmd['-data'])
	rankData()


# argv -data data.json
main()


