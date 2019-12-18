import ast
import json
import os
import sys
from nltk import ngrams
import ntpath
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

positive_word = {}
negative_word = {}
emoticon = {}
plain_emoticon = {}


def has_numbers(input_string):
	return any(char.isdigit() for char in input_string)


def read_json(json_file):
	return json.loads(read_file(json_file))


def read_file(path_file):
	return os.popen('cat ' + str(path_file)).read()


def get_all_files_in_path(path_folder):
	return os.popen('ls ' + str(path_folder)).read().split('\n')


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


def features(src, dst):
	files = get_all_files_in_path(src)

	for file in files:
		if ntpath.basename(file) == '':
			continue
		text_file = read_file(src + file)
		for line in text_file.split("\n"):
			line_features = []
			if len(line) == 0:
				continue
			data = json.loads(json.loads(line))
			text = features_text(data['text'])
			emoji_p = features_emoji(data['emoji'])
			emoji_n = features_emoji(data['emoji'])
			line_features += text + [emoji_p] + [emoji_n]
			feats = label_candidate(line_features)
			line_features += [str(data['date'])] + [str(data['time'])] + [str(data['mention'])] + [str(data['hashtags'])] + [feats]
			print(line_features)


def main():
	counter = 1
	cmd = {}

	# for get cmd with -flag
	for cmdLine in sys.argv[1:]:
		if cmdLine[:1] == '-' and counter + 1 < len(sys.argv):
			cmd[cmdLine] = sys.argv[counter + 1]
		counter += 1

	load_thesaurus(cmd['-positive'], cmd['-negative'])
	load_emoticon(cmd['-emoticon'])
	features(cmd['-src'], cmd['-dst'])


# argv -src path-data -dst path-dst -positive file-path -negative file-path -stop-word file-path -emoticon path-emoticon
main()
