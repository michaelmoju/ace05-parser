from annotation.annotation import Annotation, Mention, Extent


class Relation(Annotation):
	def __init__(self, annot):
		super().__init__(annot)
		for mention in annot:
			if mention.tag == 'relation_mention':
				self.mentions.append(RelationMention(mention))

	def get_dict(self):
		relation_dict = {'relationID': self.id,
					   'relationType': self.type,
					   'relationSubType': self.subtype,
					   'relationMentionList': [mention.get_dict() for mention in self.mentions]}
		return relation_dict

class RelationMention(Mention):
	def __init__(self, mention):
		super().__init__()
		self.id = mention.get('ID')
		for mention_child in mention:
			if mention_child.tag == 'extent':
				self.extent = Extent(mention_child)
			elif mention_child.tag == 'relation_mention_argument':
				if mention_child.get('ROLE') == 'Arg-1':
					self.arg1 = RelationMentionArg(mention_child)
				elif mention_child.get('ROLE') == 'Arg-2':
					self.arg2 = RelationMentionArg(mention_child)

	def get_dict(self):
		mention_dict = {'mention_id': self.id,
						'extent': self.extent.text, 'start': self.extent.start, 'end': self.extent.end,
						'mentionArg1': self.arg1.get_dict(), 'mentionArg2': self.arg2.get_dict()}
		return mention_dict

class RelationMentionArg(Mention):
	def __init__(self, mention_child):
		super().__init__()
		self.id = mention_child.get('REFID')
		self.extent = Extent(mention_child[0])

	def get_dict(self):
		arg_dict = {'argMentionid': self.id,
					'extent': self.extent.text,
					'start': self.extent.start,
					'end': self.extent.end}
		return arg_dict
