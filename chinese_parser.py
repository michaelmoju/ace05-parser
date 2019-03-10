import json
import os
import glob
import xml.etree.ElementTree as ET


def parse_sgm(fh):
	tree = ET.parse(fh)
	root = tree.getroot()

	assert root.tag == 'DOC'

	for child in root:
		if child.tag == 'BODY':
			TEXT = child[0]
			for turns in TEXT:
				print(turns.text.replace(" ", "").replace("\n", ""))


def parse_sgms(path):
	files = glob.glob(path+'*.sgm')
	for f in files:
		parse_sgm(f)


if __name__ == '__main__':
	import argparse

	DEBUG = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', default='./Data/LDC2006T06/data/Chinese/')

	args = parser.parse_args()

	data_path = args.data_path

	bn_path = data_path + 'bn/adj/'
	nw_path = data_path + 'nw/adj/'
	wl_path = data_path + 'wl/adj/'

	parse_sgms(bn_path)




