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
			bn_dic['DOCID'] = child.text
		elif child.tag == 'BODY':
			TEXT = child[0]
			for turn in TEXT:
				print(turn.text.replace(" ", "").replace("\n", ""))
				turns.append(turn)

	#################################

	doc_chars = []

	with open(fh) as f:
		for l in f:
			l = re.sub('<.*?>', '', l)
			for c in l:
				doc_chars.append(c)

	bn_dic['turns'] = turns
	bn_dic['doc_chars'] = doc_chars

	return bn_dic


def nw_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()

	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'BODY':
			TEXT = child[0]
			for turns in TEXT:
				print(turns.text.replace(" ", "").replace("\n", ""))


def wl_parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()

	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'BODY':
			TEXT = child[0]
			for turns in TEXT:
				print(turns.text.replace(" ", "").replace("\n", ""))


def parse_sgms(path):

	if 'bn' in path:
		files = glob.glob(path+'*.sgm')
		for f in files:
			bn_dic = bn_parse_sgm(f)

	elif 'nw' in path:
		files = glob.glob(path + '*.sgm')
		for f in files:
			nw_parse_sgm(f)

	elif 'wl' in path:
		files = glob.glob(path + '*.sgm')
		for f in files:
			wl_parse_sgm(f)


if __name__ == '__main__':
	bn_parse_sgm('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/CBS20001001.1000.0041.sgm')



