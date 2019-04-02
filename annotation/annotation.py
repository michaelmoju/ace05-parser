class Annotation:
	def __init__(self, annot):
		self.id = annot.get('ID')
		self.type = annot.get('TYPE')
		self.subtype = annot.get('SUBTYPE')
		self.mentions = []


class Mention:
	def __init__(self):
		self.id = ''
		self.extent = Extent

class Extent:
	def __init__(self, mention_child):
		self.text = mention_child[0].text
		self.start = int(mention_child[0].get('START'))
		self.end = int(mention_child[0].get('END'))
