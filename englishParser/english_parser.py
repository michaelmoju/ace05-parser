from englishParser.english_sgm_parser import *


if __name__ == '__main__':
	import argparse

	DEBUG = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', default='./Data/LDC2006T06/data/English/')

	args = parser.parse_args()

	data_path = args.data_path

	bn_path = data_path + 'bn/adj/'
	nw_path = data_path + 'nw/adj/'
	wl_path = data_path + 'wl/adj/'

	parse_sgms(bn_path)