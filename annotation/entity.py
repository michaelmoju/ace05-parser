from annotation.annotation import Annotation, Mention, Extent


class Entity(Annotation):
	def __init__(self, annot):
		super().__init__(annot)
		for mention in annot:
			if mention.tag == 'entity_mention':
				self.mentions.append(EntityMention(mention))

	def get_dict(self):
		entity_dict = {'entityID': self.id,
					   'entityType': self.type,
					   'entitySubType': self.subtype,
					   'entityMentionList': [mention.get_dict() for mention in self.mentions]}
		return entity_dict

class EntityMention(Mention):
	def __init__(self, mention):
		super().__init__()
		self.id = mention.get('ID')
		for mention_child in mention:
			if mention_child.tag == 'extent':
				self.extent = Extent(mention_child)
			elif mention_child.tag == 'head':
				self.head = Extent(mention_child)

	def get_dict(self):
		mention_dict = {'mention_id': self.id,
						'extent': self.extent.text, 'start': self.extent.start, 'end': self.extent.end}
		return mention_dict

