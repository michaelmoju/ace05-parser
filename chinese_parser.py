from chinese_sgm_parser import *


def get_relations_from_file(docID, sgm_dics):
	v = sgm_dics.get(docID)
	text = ''
	sentences = {}
	sentence_data = {}
	id = 0

	string = ''
	for index, t in enumerate(v):
		text += t
		string += t
		if t == '。':
			sentence_data['string'] = string
			sentence_data['start'] = index - (len(string) - 1)
			sentence_data['end'] = index
			sentences[id] = sentence_data
			sentence_data = {}
			string = ''
			id += 1
	print(text)

	for k, v in sentences.items():
		if "\n\n" in v['string']:
			o_len = len(v['string'])
			sentences[k]['string'] = re.sub('.*\n\n?', '', v['string'])
			redun_len = o_len - len(sentences[k]['string'])
			sentences[k]['start'] += redun_len

	print(sentences)


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

	sgm_dics = parse_sgms(bn_path)

	get_relations_from_file(' CBS20001001.1000.0041 ', sgm_dics)





