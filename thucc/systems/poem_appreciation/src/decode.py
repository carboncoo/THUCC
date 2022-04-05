#!python3
# encoding: utf-8

import math
from util import isPunctuation

def computeScore(poem, keywords, keywords_characters):
	scores = []
	for keyword, keyword_count in keywords.items():
		keywords_characters_sum = sum(keywords_characters[keyword].values())
		score = sum((-1000 if keywords_characters[keyword][c] == 0 else math.log(keywords_characters[keyword][c])) 
					- math.log(keywords_characters_sum) 
				for c in poem if not c.isspace() and not isPunctuation(c))
		score += math.log(keyword_count)
		scores.append((keyword, score))
	return sorted(scores, key=lambda x: x[1], reverse=True)

def generateAppreciation(scores, num):
	num = min(num, len(scores))
	verbs = set()
	result = '本诗'
	for i in range(len(scores)):
		clause = scores[i][0] #output_templates[i % len(output_templates)].replace('(.*?)', scores[i][0])
		verb = clause[0:2]
		if not verb in verbs:
			verbs.add(verb)
			result += clause
			if len(verbs) < num:
				result += '，'
			else:
				result += '。'
				break
	return result
