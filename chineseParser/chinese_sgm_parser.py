import glob
import xml.etree.ElementTree as ET
import json
import re
from annotation.sgm import SgmDoc


def parse_sgm_to_SgmDoc(fh):
	tree = ET.parse(fh)
	root = tree.getroot()
	assert root.tag == 'DOC'

	doc_id = ''
	for child in root:
		if child.tag == 'DOCID':
			doc_id = child.text.strip()

	doc_chars = []
	with open(fh) as f:
		for l in f:
			l = re.sub('<.*?>', '', l)
			for c in l:
				doc_chars.append(c)

	return SgmDoc(doc_id, doc_chars)


def bn_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()
	bn_dic = {}
	turns = []
	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'DOCID':
			# print(child.text)
			bn_dic['DOCID'] = child.text.strip()
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
			nw_dic['DOCID'] = child.text.strip()
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
			wl_dic['DOCID'] = child.text.strip()
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

	return wl_dic


def parse_sgms(path):
	dicts = {}
	files = glob.glob(path + '*.sgm')
	for f in files:
		mySgmDoc = parse_sgm_to_SgmDoc(f)
		mySgmDoc.sentence_split()
		dicts[mySgmDoc.doc_id] = mySgmDoc

	return dicts


if __name__ == '__main__':

	dicts = parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/wl/adj/')
	print(dicts["DAVYZW_20041223.1020"].doc_chars[100:200])
	print(dicts["DAVYZW_20041223.1020"].sentence_list[0].start)
	print(dicts["DAVYZW_20041223.1020"].sentence_list[0].end)
	print(dicts["DAVYZW_20041223.1020"].sentence_list[0].string)

	# dicts = parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
	# print(dicts["CBS20001001.1000.0041"].sentence_list[0].string)
