import re
import json

class Word:
	def __init__(self, string, start, end):
		self.string = string
		self.start = start
		self.end = end

class Sentence:
	def __init__(self, string, start, end):
		self.string = string
		self.start = start
		self.end = end
		self.words = []

	def to_words(self, t):
		self.words.append(Word(t['word'], t['characterOffsetBegin'], t['characterOffsetEnd']-1))

	def clean_first_sentence(self):
		if "\n\n" in self.string:
			o_len = len(self.string)
			self.string = re.sub('.*\n\n?', '', self.string)
			redun_len = o_len - len(self.string)
			self.start += redun_len
		if re.match('.* \n?', self.string):
			o_len = len(self.string)
			self.string = re.sub('.* \n?', '', self.string)
			redun_len = o_len - len(self.string)
			self.start += redun_len

class SgmDoc:
	def __init__(self, docid, doc_chars):
		self.doc_id = docid
		self.doc_chars = doc_chars
		self.sentence_list = []

	def sentence_split(self):
		string = ''
		id = 0
		for index, t in enumerate(self.doc_chars):
			string += t

			# sentence segmentation
			if t == '。':
				mySentence = Sentence(string=string, start=index - (len(string) - 1), end=index)
				# if id == 0:
				# 	mySentence.clean_first_sentence()

				self.sentence_list.append(mySentence)
				id += 1
				string = ''

