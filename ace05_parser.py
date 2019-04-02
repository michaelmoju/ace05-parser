import chinese_sgm_parser
from englishParser import english_sgm_parser
import argparse
import re


def get_relations_from_file(docID, sgm_dics):
	v = sgm_dics.get(' CBS20001001.1000.0041 ')
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

	parser = argparse.ArgumentParser()
	parser.add_argument('language', choices=['chinese', 'english'])
	parser.add_argument('--corenlp_path', default='http://140.109.19.190')

	args = parser.parse_args()

	lang = args.language
	corenlp = args.corenlp_path

	if lang == 'chinese':
		# chinese_sgm_parser.parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/nw/adj/')
		sgm_dics = chinese_sgm_parser.parse_sgms('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
		v = sgm_dics.get(' CBS20001001.1000.0041 ')
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
				sentence_data['start'] = index - (len(string)-1)
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

		# for k, v in sgm_dics.items():
		# 	text = ''
		# 	for t in v:
		# 		text += t
		# 	text.replace("\n", "").replace(" ", "")
		# 	ssplit_sgm_dics[k] = text
		#
		# with StanfordCoreNLP(corenlp, port=9000) as nlp:
		# 	props={'annotators': 'tokenize,ssplit', 'pipelineLanguage': 'zh', 'outputFormat': 'json'}
		# 	for k, v in ssplit_sgm_dics.items():
		# 		print(k)
		# 		print(nlp.annotate(v), props)

	elif lang == 'english':
		english_sgm_parser.parse_sgms('')

