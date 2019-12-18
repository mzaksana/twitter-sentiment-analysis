import ast
import json
import os
import sys
from nltk import ngrams
from sklearn.metrics import classification_report, confusion_matrix
import re
import regex
import emoji
import ntpath
import pandas as pd
import numpy as np
import struct
import matplotlib.pyplot as plt
import sys
import json
import seaborn as sn


positive_word = {}
negative_word = {}
emoticon = {}
plain_emoticon = {}

model = None
class_labels = None

struct.calcsize("P") * 8



def has_numbers(input_string):
	return any(char.isdigit() for char in input_string)


def read_json(json_file):
	return json.loads(read_file(json_file))


def read_file(path_file):
	return os.popen('cat ' + str(path_file)).read()


def get_all_files_in_path(path_folder):
	return os.popen('ls ' + str(path_folder)).read().split('\n')

def extractEmojis(text):
	emoji_list = []
	data = regex.findall(r'\X', text)
	for word in data:
		if any(char in emoji.UNICODE_EMOJI for char in word):
			emoji_list.append(word)
	return emoji_list

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

def load_stop_words(file_stop_words):
	stop_words = {}
	stopwords_data = read_file(file_stop_words).split('\n')
	for stopword in stopwords_data:
		stop_words[stopword] = 1


def load_emoticon(emoticon_file):
	global emoticon
	data = read_file(emoticon_file).split('\n')
	for line in data:
		f = line.split(',')
		if len(f) < 3:
			continue

		if f[1] == 1:
			emoticon[f[0]] = -1
		elif f[2] == 1:
			emoticon[f[0]] = 0
		elif f[3] == 1:
			emoticon[f[0]] = 1


def load_thesaurus(positive_file, negative_file):
	global positive_word
	global negative_word

	data = read_file(positive_file).split('\n')
	for line in data:
		positive_word[line] = 1
	data = read_file(negative_file).split('\n')
	for line in data:
		negative_word[line] = 1


def is_set(variable):
	return variable in locals() or variable in globals()


# flag : pos or nev
def negation(term, flag):
	return [-1]


def positive(text, n_grams):
	global positive_word
	score = 0
	if n_grams == 3:
		if text[0] in ["sangat", "amat", "terlalu"]:
			score += 1
			if text[1] in positive_word:
				score += 1
				if text[2] in positive_word:
					score += 1
		if text[0] in positive_word:
			score += 1
			if text[1] in positive_word:
				score += 1

	elif n_grams == 2:
		if text[0] in ["tidak", "bukan"]:
			score += 1
			if text[1] in negative_word:
				score += 1

	else:
		score = 1 if text[0] in positive_word else 0
	return score

def negative(text, n_grams):
	score = 0
	if n_grams == 3:
		if text[0] in ["sangat", "amat", "terlalu"]:
			score += 1
			if text[1] in negative_word:
				score += 1
				if text[2] in positive_word:
					score += 1
		if text[0] in negative_word:
			score += 1
			if text[1] in positive_word:
				score += 1
	elif n_grams == 2:
		if text[0] in ["tidak", "bukan"]:
			score += 1
			if text[1] in positive_word:
				score += 1
	else:
		score = 1 if text[0] in negative_word else 0
	return score * -1

def features_text(text):
	result = [0] * 6
	n_grams = [1, 2, 3]
	counter = 0
	for n_gram in n_grams:
		text_grams = ngrams(text.split(), n_gram)
		for term in text_grams:
			result[counter] += positive(term, n_gram)
			result[counter + 3] += negative(term, n_gram)
		counter += 1
	return result


def features_emoji(emoticons_l):
	global emoticon
	score = 0
	for emotic in emoticons_l:
		if emotic in emoticon:
			score += emoticon[emotic]
	return score


def label_candidate(data_features):
	score = 0
	for data in data_features:
		score += data
	if score > 0:
		return "positive"
	if score < 0:
		return "negative"
	return "neutral"


def features(data):
	line_features = []
	text = features_text(cleanText(clean_format(data)))
	emoji_p = features_emoji(extractEmojis(data))
	emoji_n = features_emoji(extractEmojis(data))
	line_features += text + [emoji_p] + [emoji_n]
	return line_features

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def sigmoid_der(x):
	return sigmoid(x) * (1 - sigmoid(x))

def softmax(A):
	expA = np.exp(A)
	return expA / expA.sum(axis=1, keepdims=True)

def test(fitur):
	global model
	global class_labels
	class_labels = model['class_labels']

	wh = model['weight_h_1']
	bh = model['bias_h_1']
	wh2 = model['weight_h_2']
	bh2 = model['bias_h_2']
	wh3 = model['weight_h_3']
	bh3 = model['bias_h_3']
	wo = model['weight_h_o']
	bo = model['bias_h_o']

	zh = np.dot(fitur, wh) + bh
	ah = sigmoid(zh)

	zh2 = np.dot(ah, wh2) + bh2
	ah2 = sigmoid(zh2)

	zh3 = np.dot(ah2, wh3) + bh3
	ah3 = sigmoid(zh3)

	zo = np.dot(ah3, wo) + bo
	result = softmax(zo)
	poll = None
	result_c = 1
	key = 0
	for label_res in result[0]:
		if poll == None :
			poll = label_res
			result_c = key
			key +=1
			continue
		if poll < label_res:
			poll = label_res
			result_c = key
		key+=1
	return class_labels[result_c]

def confusion(data_file):
	data_test = pd.read_csv(data_file, sep=',\s+', delimiter=':::', encoding="utf-8", skipinitialspace=True)
	x_tests = data_test.drop('Class', axis=1)
	# y_tests = data_test['Class']
	y_pr = []
	y_tests = []
	max=len(x_tests)

	i = 0
	for x_test in x_tests.values.tolist():
		print("test", i, "from", max)
		if len(x_test[0]) == 0:
			continue
		feats=features(x_test[0])
		y_tests += [label_candidate(feats)]
		y_pr += [test([feats])]
		i += 1
	confs=confusion_matrix(y_tests,y_pr)
	print(confs)
	print(classification_report(y_tests,y_pr))
	df_cm = pd.DataFrame(confs, index=["negative","neutral","positive"], columns=["negative","neutral","positive"])
	sn.heatmap(df_cm,annot=True,cmap='gray_r', fmt='g')

	plt.show()


def main():
	counter = 1
	cmd = {}
	global model
	global class_labels

	# for get cmd with -flag
	for cmdLine in sys.argv[1:]:
		if cmdLine[:1] == '-' and counter + 1 < len(sys.argv):
			cmd[cmdLine] = sys.argv[counter + 1]
		counter += 1

	load_thesaurus(cmd['-positive'], cmd['-negative'])
	load_emoticon(cmd['-emoticon'])

	model = np.load(cmd['-model'])
	confusion(cmd['-test'])

# argv -model model.npz -test test-file.csv
main()
