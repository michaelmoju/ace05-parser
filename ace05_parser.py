from chineseParser import chinese_sgm_parser
from englishParser import english_sgm_parser
import argparse
import re
import json
from stanfordcorenlp import StanfordCoreNLP
from annotation.sgm import SgmDoc, Sentence


def get_SgmDoc_from_file(docID, sgm_dics):
	v = sgm_dics.get(docID)
	text = ''
	id = 0

	mySgmDoc = SgmDoc()
	string = ''
	for index, t in enumerate(v):
		text += t
		string += t

		# sentence segmentation
		if t == '。':
			mySentence = Sentence(string=string, start=index - (len(string) - 1), end=index)
			if id == 0:
				mySentence.clean_first_sentence()
			mySgmDoc.append_sent(mySentence)
			id += 1
	print(text)
	return mySgmDoc

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('language', choices=['chinese', 'english'])
	parser.add_argument('--corenlp_path', default='http://140.109.19.190')

	args = parser.parse_args()

	lang = args.language
	corenlp = args.corenlp_path

	if lang == 'chinese':
		sgm_dics = chinese_sgm_parser.parse_sgms(
			'/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
		mySgmDoc = get_SgmDoc_from_file('CBS20001001.1000.0041', sgm_dics)

		with StanfordCoreNLP(corenlp, port=9000) as nlp:
			props={'annotators': 'tokenize', 'pipelineLanguage': 'zh', 'outputFormat': 'json'}
			for k, v in sentences.items():
				print(k)
				annotation = nlp.annotate(v['string'], props)
				print(annotation)
				annotation = json.loads(annotation)
				print(annotation['tokens'])

	elif lang == 'english':
		english_sgm_parser.parse_sgms('')

