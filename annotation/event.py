from annotation.annotation import Annotation, Mention, Extent


class Event(Annotation):
	def __init__(self, annot):
		super().__init__(annot)
		self.arg_list = []
		for child in annot:
			if child.tag == 'event_argument':
				self.arg_list.append(EventArg(child))
			elif child.tag == 'event_mention':
				self.mentions.append(EventMention(child))

	def get_dict(self):
		event_dict = {'eventID': self.id,
					  'eventType': self.type,
					  'eventSubType': self.subtype,
					  'eventArgList': [arg.get_dict() for arg in self.arg_list],
					  'eventMentionList': [mention.get_dict() for mention in self.mentions]}
		return event_dict

class EventArg:
	def __init__(self, annot_child):
		self.id = annot_child.get('REFID')
		self.role = annot_child.get('ROLE')

	def get_dict(self):
		arg_dict = {'id': self.id, 'role': self.role}
		return arg_dict

class EventMention(Mention):
	def __init__(self, mention):
		super().__init__()
		self.id = mention.get('ID')
		self.mention_arg_list = []

		for mention_child in mention:
			if mention_child.tag == 'extent':
				self.extent = Extent(mention_child)
			elif mention_child.tag == 'anchor':
				self.anchor = Extent(mention_child)
			elif mention_child.tag == 'event_mention_argument':
				self.mention_arg_list.append(EventMentionArg(mention_child))

	def get_dict(self):
		mention_dict = {'id': self.id,
						'extent': self.extent.text, 'start': self.extent.start, 'end': self.extent.end,
						'anchor': self.anchor.text,
						'mentionArgList': [mention_arg.get_dict() for mention_arg in self.mention_arg_list]}
		return mention_dict

class EventMentionArg:
	def __init__(self, mention_child):
		self.id = mention_child.get('REFID')
		self.role = mention_child.get('ROLE')
		self.extent = Extent(mention_child[0])

	def get_dict(self):
		mention_arg_dict = {'id': self.id,
							'role': self.role,
							'extent': self.extent.text,
							'start': self.extent.start,
							'end': self.extent.end}
		return mention_arg_dict