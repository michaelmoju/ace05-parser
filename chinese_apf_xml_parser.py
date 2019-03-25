import glob
import xml.etree.ElementTree as ET


def parse_apf(fh):
	entity_dics = {}
	relation_list = []
	event_dic = {}

	tree = ET.parse(fh)
	root = tree.getroot()

	assert root.tag == 'source_file'

	dicID = root[0].get('DOCID')

	for annot in root[0]:
		if annot.tag == 'entity':
			entity_dic = {}
			e_mention_list = []
			entity_dic['entityType'] = annot.get('TYPE')
			entity_dic['entitySubType'] = annot.get('SUBTYPE')
			entity_dic['entityID'] = annot.get('ID')

			for mention in annot:
				mention_dic = {}
				mention_dic['mention_id'] = mention.get('ID')
				mention_dic['extent'] = mention[0][0].text
				mention_dic['start'] = mention[0][0].get('START')
				mention_dic['end'] = mention[0][0].get('END')
				e_mention_list.append(mention_dic)
			entity_dic['entityMentionList'] = e_mention_list

			entity_dics[annot.get('ID')] = entity_dic

		elif annot.tag == 'relation':
			relation_dic = {}

			relation_dic['relationID'] = annot.get('ID')
			relation_dic['relationType'] = annot.get('TYPE')
			relation_dic['relationSubType'] = annot.get('SUBTYPE')

			for child in annot:
				if child.tag == 'relation_mention':
					mentionArg1_dic = {}
					mentionArg2_dic = {}

					relation_dic['id'] = child.get('ID')
					for mention_child in child:
						if mention_child.tag == 'extent':
							relation_dic['extent'] = mention_child[0].text

						if mention_child.tag == 'relation_mention_argument':
							if mention_child.get('ROLE') == 'Arg-1':
								mentionArg1_dic['argMentionid'] = mention_child.get('REFID')
								mentionArg1_dic['extent'] = mention_child[0][0].text
								mentionArg1_dic['start'] = mention_child[0][0].get('START')
								mentionArg1_dic['end'] = mention_child[0][0].get('END')
								relation_dic['mentionArg1'] = mentionArg1_dic
							elif mention_child.get('ROLE') == 'Arg-2':
								mentionArg2_dic['extent'] = mention_child.get('REFID')
								mentionArg2_dic['argMentionid'] = mention_child[0][0].text
								mentionArg2_dic['start'] = mention_child[0][0].get('START')
								mentionArg2_dic['end'] = mention_child[0][0].get('END')
								relation_dic['mentionArg2'] = mentionArg2_dic
					relation_list.append(relation_dic)

		elif annot.tag == 'event':
			# TODO
			continue

	# print(entity_dics)
	# print(relation_list)

	return dicID, entity_dics, relation_list, event_dic


def parse_apfs_relations(fp):

	dic2relations = {}

	files = glob.glob(fp + '*.apf.xml')
	for f in files:
		dicID, entity_dics, relation_list, event_dic = parse_apf(f)
		dic2relations[dicID] = relation_list

	return dic2relations


if __name__ == '__main__':
	# parse_apf('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/CBS20001001.1000.0041.apf.xml')

	dic2relations = parse_apfs_relations('/media/moju/data/work/ace05-parser/Data/LDC2006T06/data/Chinese/bn/adj/')
	print(dic2relations['CBS20001001.1000.0041'])

