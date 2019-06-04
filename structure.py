from typing import *


class Token:
	def __init__(self, id: int, text: str, pos: str):
		self.id = id
		self.text = text
		self.pos = pos
		
class EntityMention:
	def __init__(self, id: str=None, entity_id: str=None, type: str=None, text: str=None, char_b: int=None, char_e: int=None,
	             tokens: List[Token]=None, token_b: int=None, token_e: int=None):
		self.id = id
		self.entity_id = entity_id
		self.type = type
		self.text = text
		self.char_b = char_b
		self.char_e = char_e
		self.tokens = tokens
		self.token_b = token_b
		self.token_e = token_e

	def __str__(self):
		return "extent:{}\t".format(self.extent) + "etype:{}".format(self.etype)

	def set_entity(self, entity):
		self.entity = entity

	def set_sentence(self, sentence):
		self.sentence = sentence

	def set_document(self, document):
		self.doc = document

	def set_cluster(self, cluster):
		self.cluster = cluster


class RelationMention:
	def __init__(self, id: int, type: str, arg1: EntityMention, arg2: EntityMention):
		self.id = id
		self.type = type
		self.arg1 = arg1
		self.arg2 = arg2

	def set_sentence(self, sentence):
		self.sentence = sentence

	def set_document(self, document):
		self.doc = document


class Sentence:
	def __init__(self, id: int=None, docID: str=None, tokens: List[Token]=None, text: str=None, char_b: int=None, char_e: int=None,
				 entity_mentions: List[EntityMention]=None, relation_mentions: List[RelationMention]=None):
		self.id = id
		self.docID = docID
		self.tokens = tokens
		self.text = text
		self.char_b = char_b
		self.char_e = char_e
		self.entity_mentions = entity_mentions
		self.relation_mentions = relation_mentions

	def __str__(self):
		e_mentions_string = ''
		for e in self.entity_mentions:
			e_mentions_string += str(e) + '\t'
		return "sent_index:{}\n".format(self.id) + "text:{}\n".format(self.text) + \
				"e_mentions:\n" + e_mentions_string


class Document:
	def __init__(self, id: str, sentences: List[Sentence]):
		self.id = id
		self.sentences = sentences

	def set_cluster(self, cluster):
		self.cluster = cluster


class Cluster:
	def __init__(self, id: int, documents: List[Document]):
		self.id = id
		self.documents = documents


# after coreference
class Entity:
	def __init__(self, id: int, mentions: List[EntityMention]):
		self.id = id
		self.mentions = mentions
