from structure import *
from chineseParser import chinese_parser
from englishParser import english_parser

class ACE05Reader:
	def __init__(self, lang: str):
		self.lang = lang
	
	def read(self, fp) -> Dict[str, Document]:
		doc_dicts = {}
		if self.lang == 'en':
			data_path = fp + 'English/'
			english_parser.parse_source(data_path)
			return doc_dicts
		elif self.lang == 'zh':
			data_path = fp + 'Chinese/'
			chinese_parser.parse_source(data_path)
			return doc_dicts



