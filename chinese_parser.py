from chinese_sgm_parser import *
from chinese_apf_xml_parser import *
import json
import glob
import os


def is_in_sentence(index, sentence_start, sentence_end):



def clean_string(string):
	out_string = ''
	for t in string:
		if not (t == "\n" or t == " "):
			out_string += t
	return out_string


def index_clean(sent_start, sent_string, arg_index):
	arg_index -= sent_start
	delete_n = 0
	for t_index, t in enumerate(sent_string):
		if t == "\n" or t == " ":
			assert (arg_index!=t_index)
			if arg_index > t_index:
				# print('arg_index:{}'.format(arg_index))
				# print('t_index:{}'.format(t_index))
				delete_n += 1
	# print('delete_n:{}'.format(delete_n))
	return arg_index - delete_n


def get_relations_from_file(docID, sgm_dics, dic2relations):

	doc_chars = sgm_dics[docID]
	text = ''
	sentences = {}
	sentence_data = {}
	id = 0

	string = ''
	for index, t in enumerate(doc_chars):
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

	if "\n\n" in sentences[0]['string']:
		o_len = len(sentences[0]['string'])
		sentences[0]['string'] = re.sub('.*\n\n?', '', sentences[0]['string'])
		redun_len = o_len - len(sentences[0]['string'])
		sentences[0]['start'] += redun_len
	elif " \n" in sentences[0]['string']:
		o_len = len(sentences[0]['string'])
		sentences[0]['string'] = re.sub('.* \n?', '', sentences[0]['string'])
		redun_len = o_len - len(sentences[0]['string'])
		sentences[0]['start'] += redun_len

	# for k, v in sentences.items():
	# 	if "\n\n" in v['string']:
	# 		o_len = len(v['string'])
	# 		sentences[k]['string'] = re.sub('.*\n\n?', '', v['string'])
	# 		redun_len = o_len - len(sentences[k]['string'])
	# 		sentences[k]['start'] += redun_len

	relation_list = dic2relations[docID.strip()]

	for relation_mention in relation_list:
		mention_extent_start = relation_mention['start']
		mention_extent_end = relation_mention['end']

		for sentence_index, sentence in sentences.items():
			if sentence['start'] <= mention_extent_start <= sentence['end']:

				if not (sentence['start'] <= mention_extent_end <= sentence['end']):
					print('Relation extent over sentence boundary! Remove this relation mention.')
					print(sentence['string'])

				relation_mention['mentionArg1']['start'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg1']['start'])
				relation_mention['mentionArg1']['end'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg1']['end'])
				relation_mention['mentionArg1']['extent'] = clean_string(relation_mention['mentionArg1']['extent'])
				relation_mention['mentionArg2']['start'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg2']['start'])
				relation_mention['mentionArg2']['end'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg2']['end'])
				relation_mention['mentionArg2']['extent'] = clean_string(relation_mention['mentionArg2']['extent'])

				relation_mention['start'] = index_clean(sentence['start'], sentence['string'], relation_mention['start'])
				relation_mention['end'] = index_clean(sentence['start'], sentence['string'], relation_mention['end'])
				relation_mention['extent'] = clean_string(relation_mention['extent'])

				relation_mention['sentence_index'] = sentence_index

				relation_mention['Tokens'] = []
				for t in sentence['string']:
					if not (t == "\n" or t == " "):
						relation_mention['Tokens'].append(t)
				relation_mention['sentence_length'] = len(relation_mention['Tokens'])

	return relation_list


def get_relation_from_files(dir, outpath):
	files = glob.glob(dir + '*.sgm')
	for f in files:
		docID = os.path.splitext(os.path.basename(f))[0]

		sgm_dics = parse_sgms(dir)
		dic2relations = parse_apfs_relations(dir)
		relation_list = get_relations_from_file(docID, sgm_dics, dic2relations)

		with open(outpath+docID+'.relationMention.json', 'w') as f:
			json.dump(relation_list, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	import argparse

	DEBUG = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', default='./Data/LDC2006T06/data/Chinese/')
	parser.add_argument('--output_path', default='./output/')

	args = parser.parse_args()

	data_path = args.data_path
	output_path = args.output_path

	bn_path = data_path + 'bn/adj/'
	nw_path = data_path + 'nw/adj/'
	wl_path = data_path + 'wl/adj/'

	get_relation_from_files(bn_path, output_path+'bn/adj/')

	# sgm_dics = parse_sgms(wl_path)
	# dic2relations = parse_apfs_relations(wl_path)
	#
	# relation_list = get_relations_from_file('DAVYZW_20050105.1242', sgm_dics, dic2relations)
	#
	# with open('output/test.json', 'w') as f:
	#
	# 	json.dump(relation_list, f, indent=4, ensure_ascii=False)






