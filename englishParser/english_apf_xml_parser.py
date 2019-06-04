import glob
import xml.etree.ElementTree as ET
from annotation.apfentity import ApfEntity
from annotation.apfrelation import ApfRelation
from annotation.event import Event

def parse_apf(fh):
	entity_dicts = {}
	relation_dicts = {}
	event_dicts = {}

	tree = ET.parse(fh)
	root = tree.getroot()

	assert root.tag == 'source_file'

	docID = root[0].get('DOCID')

	for annot in root[0]:
		if annot.tag == 'entity':
			entity = ApfEntity(annot)
			entity_dicts[entity.id] = entity.get_dict()

		elif annot.tag == 'relation':
			relation = ApfRelation(annot)
			relation_dicts[relation.id] = relation.get_dict()

		elif annot.tag == 'event':
			event = Event(annot)
			event_dicts[event.id] = event.get_dict()

	return docID, entity_dicts, relation_dicts, event_dicts

def parse_apf_docs(fp):
	doc2entities = {}
	doc2relations = {}
	doc2events = {}

	files = glob.glob(fp + '*.apf.xml')
	for f in files:
		docID, entity_dicts, relation_dicts, event_dicts = parse_apf(f)
		doc2entities[docID] = entity_dicts
		doc2relations[docID] = relation_dicts
		doc2events[docID] = event_dicts

	return doc2entities, doc2relations, doc2events


if __name__ == '__main__':

	doc2entities, doc2relations, doc2events = parse_apfs_doc(
		'/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/English/bc/adj/')
	print(doc2entities['CNN_CF_20030303.1900.00'])
	print(doc2relations['CNN_CF_20030303.1900.00'])
	print(doc2events['CNN_CF_20030303.1900.00'])