from chinese_sgm_parser import *
from chinese_apf_xml_parser import *


def index_clean(sent_start, sent_string, arg_index):
	for t_index, t in enumerate(sent_string):
		if t == "\n" or " ":
			assert (arg_index!=t_index)
			if arg_index > t_index:
				arg_index -= 1

	return arg_index - sent_start


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

	for k, v in sentences.items():
		if "\n\n" in v['string']:
			o_len = len(v['string'])
			sentences[k]['string'] = re.sub('.*\n\n?', '', v['string'])
			redun_len = o_len - len(sentences[k]['string'])
			sentences[k]['start'] += redun_len

	relation_list = dic2relations[docID.strip()]

	print(sentences)

	for relation_mention in relation_list:
		for sentence_index, sentence in sentences.items():
			if (sentence['start'] <= relation_mention['start'] <= sentence['end']):
				assert (sentence['start'] <= relation_mention['end'] <= sentence['end'])

				# DEBUG this
				relation_mention['sentence_length'] = sentence['end'] - sentence['start'] + 1
				relation_mention['mentionArg1']['start'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg1']['start'])
				relation_mention['mentionArg1']['end'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg1']['end'])
				relation_mention['mentionArg2']['start'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg2']['start'])
				relation_mention['mentionArg2']['end'] = index_clean(sentence['start'], sentence['string'], relation_mention['mentionArg2']['end'])

				relation_mention['sentence_index'] = sentence_index

				relation_mention['Tokens'] = []
				for t in sentence['string']:
					if not (t == "\n" or t == " "):
						relation_mention['Tokens'].append(t)

				assert len(relation_mention['Tokens']) == relation_mention['sentence_length']
	return relation_list


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
	dic2relations = parse_apfs_relations(bn_path)

	relation_list = get_relations_from_file(' CBS20001001.1000.0041 ', sgm_dics, dic2relations)
	print(relation_list)





