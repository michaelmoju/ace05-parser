from englishParser import english_sgm_parser
from chineseParser import chinese_sgm_parser
from structure import Sentence


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
			mySentence = Sentence(id, docID, end=index)
			if id == 0:
				mySentence.clean_first_sentence()
			mySgmDoc.append_sent(mySentence)
			id += 1
	print(text)
	return mySgmDoc

class ACE05Reader:
	def __init__(self, lang:str):
		self.lang = lang
	
	def read(self, fp):
		if self.lang == 'en':
			english_sgm_parser.parse_sgms('')
		elif self.lang == 'zh':
			sgm_dics = chinese_sgm_parser.parse_sgms(
				'/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
			mySgmDoc = get_SgmDoc_from_file('CBS20001001.1000.0041', sgm_dics)



