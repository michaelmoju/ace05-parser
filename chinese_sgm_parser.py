import glob
import xml.etree.ElementTree as ET
import json
import re


def bn_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()
	bn_dic = {}
	turns = []
	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'DOCID':
			# print(child.text)
			bn_dic['DOCID'] = child.text
		elif child.tag == 'BODY':
			TEXT = child[0]
			for turn in TEXT:
				turns.append(turn.text.replace(" ", "").replace("\n", ""))

	#################################

	doc_chars = []

	with open(fh) as f:
		for l in f:
			l = re.sub('<.*?>', '', l)
			for c in l:
				doc_chars.append(c)
	bn_dic['TURN'] = turns
	bn_dic['doc_chars'] = doc_chars

	return bn_dic


def nw_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()
	nw_dic = {}
	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'DOCID':
			nw_dic['DOCID'] = child.text
		elif child.tag == 'BODY':
			HEADLINE = child[0]
			nw_dic['HEADLINE'] = HEADLINE.text.replace(" ", "").replace("\n", "")
			for TEXT in HEADLINE:
				nw_dic['TEXT'] = TEXT.text.replace(" ", "").replace("\n", "")

	#################################

	doc_chars = []

	with open(fh) as f:
		for l in f:
			l = re.sub('<.*?>', '', l)
			for c in l:
				doc_chars.append(c)
	nw_dic['doc_chars'] = doc_chars
	# print(doc_chars[155:188])

	return nw_dic


def wl_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()
	wl_dic = {}
	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'DOCID':
			wl_dic['DOCID'] = child.text
		elif child.tag == 'BODY':
			HEADLINE = child[0]
			wl_dic['HEADLINE'] = HEADLINE.text.replace(" ", "").replace("\n", "")
			TEXT = child[1]
			POST = TEXT[0]
			POSTER = POST[0]
			POSTDATE = POST[1]
			# print(POSTDATE.tail)
			# print(HEADLINE.text)

	#################################

	doc_chars = []

	with open(fh) as f:
		for l in f:
			l = re.sub('<.*?>', '', l)
			for c in l:
				doc_chars.append(c)
	wl_dic['doc_chars'] = doc_chars
	# print(doc_chars[155:188])

	return wl_dic


def parse_sgms(path):

	dics = {}

	if 'bn' in path:
		files = glob.glob(path+'*.sgm')
		for f in files:
			dic = bn_parse_sgm(f)
			dics[dic['DOCID']] = dic['doc_chars']

	elif 'nw' in path:
		files = glob.glob(path + '*.sgm')
		for f in files:
			dic = nw_parse_sgm(f)
			dics[dic['DOCID']] = dic['doc_chars']

	elif 'wl' in path:
		files = glob.glob(path + '*.sgm')
		for f in files:
			dic = wl_parse_sgm(f)
			dics[dic['DOCID']] = dic['doc_chars']

	print(len(dics))
	return dics


if __name__ == '__main__':
	# bn_parse_sgm('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/CBS20001001.1000.0041.sgm')
	# nw_parse_sgm('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/nw/adj/XIN20001001.1400.0096.sgm')
	wl_parse_sgm('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/wl/adj/DAVYZW_20041223.1020.sgm')

	# parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
	# parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/nw/adj/')
	# parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/wl/adj/')