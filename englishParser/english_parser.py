from englishParser.english_sgm_parser import *
from englishParser.english_apf_xml_parser import *
import json
import glob
import os
from structure import *
from typing import *


def is_in_sentence(index, sentence_start, sentence_end):
	if index < sentence_start:
		return False
	elif index > sentence_end:
		return False
	else:
		return True


def clean_string(string):
	out_string = ''
	for t in string:
		if not (t == "\n" or t == " "):
			out_string += t
	return out_string


def index_clean(sent_start, sent_string, arg_index):
	arg_index -= sent_start
	delete_n = 0
	for t_index, t in enumerate(sent_string):
		if t == "\n" or t == " ":
			assert (arg_index != t_index)
			if arg_index > t_index:
				# print('arg_index:{}'.format(arg_index))
				# print('t_index:{}'.format(t_index))
				delete_n += 1
	# print('delete_n:{}'.format(delete_n))
	return arg_index - delete_n


def arg_to_word_idx(mentionArg_dic, mySentence):
	out_start = None
	out_end = None
	for idx, word in enumerate(mySentence.words):
		if word.start == mentionArg_dic['start']:
			out_start = idx
		if word.end == mentionArg_dic['end']:
			out_end = idx
	
	return out_start, out_end


def preserve_relation_example(relation, rMention, out_relation_list, sentence_index, sentence, nlp, props,
                              word_seg_error):
	out_relation_mention = {}
	mentionArg1_dic = {}
	mentionArg2_dic = {}
	
	out_relation_mention['relationID'] = relation.id
	out_relation_mention['relationType'] = relation.type
	out_relation_mention['relationSubType'] = relation.subtype
	out_relation_mention['id'] = rMention.id
	
	out_relation_mention['start'] = index_clean(sentence.start, sentence.string, rMention.extent.start)
	out_relation_mention['end'] = index_clean(sentence.start, sentence.string, rMention.extent.end)
	out_relation_mention['extent'] = clean_string(rMention.extent.text)
	
	mentionArg1_dic['start'] = index_clean(sentence.start, sentence.string, rMention.arg1.extent.start)
	mentionArg1_dic['end'] = index_clean(sentence.start, sentence.string, rMention.arg1.extent.end)
	mentionArg1_dic['extent'] = clean_string(rMention.arg1.extent.text)
	
	mentionArg2_dic['start'] = index_clean(sentence.start, sentence.string, rMention.arg2.extent.start)
	mentionArg2_dic['end'] = index_clean(sentence.start, sentence.string, rMention.arg2.extent.end)
	mentionArg2_dic['extent'] = clean_string(rMention.arg2.extent.text)
	
	out_relation_mention['sentence_index'] = sentence_index
	
	out_relation_mention['chars'] = []
	for t in sentence.string:
		if not (t == "\n" or t == " "):
			out_relation_mention['chars'].append(t)
	
	sentence_string = ''
	for t in out_relation_mention['chars']:
		sentence_string += t
	
	annotation = nlp.annotate(sentence_string, props)
	annotation = json.loads(annotation)
	
	for t in annotation['tokens']:
		sentence.to_words(t)
	
	mentionArg1_dic['start'], mentionArg1_dic['end'] = arg_to_word_idx(mentionArg1_dic, sentence)
	mentionArg2_dic['start'], mentionArg2_dic['end'] = arg_to_word_idx(mentionArg2_dic, sentence)
	
	out_relation_mention['Tokens'] = [word.string for word in sentence.words]
	out_relation_mention['Sentence'] = sentence_string
	out_relation_mention['sentence_length'] = len(out_relation_mention['chars'])
	out_relation_mention['mentionArg1'] = mentionArg1_dic
	out_relation_mention['mentionArg2'] = mentionArg2_dic
	
	if not (mentionArg1_dic['start'] == None or mentionArg1_dic['end'] == None or mentionArg2_dic['start'] == None or
	        mentionArg2_dic['end'] == None):
		out_relation_list.append(out_relation_mention)
	else:
		word_seg_error += 1
	return word_seg_error


def get_relations_from_file(docID, sgm_dicts, doc2relations, nlp, props):
	out_relation_list = []
	word_seg_error = 0
	
	for relation_id, relation in doc2relations[docID].items():
		for rMention in relation.mentions:
			mention_extent_start = rMention.extent.start
			mention_extent_end = rMention.extent.end
			
			for sentence_index, sentence in enumerate(sgm_dicts[docID].sentence_list):
				if sentence.start <= mention_extent_start <= sentence.end:
					
					if not (sentence.start <= mention_extent_end <= sentence.end):
						print('Relation extent over sentence boundary!')
					# print(sentence['string'])
					
					if not (is_in_sentence(rMention.arg1.extent.start, sentence.start, sentence.end) and
					        is_in_sentence(rMention.arg1.extent.end, sentence.start, sentence.end) and
					        is_in_sentence(rMention.arg2.extent.start, sentence.start, sentence.end) and
					        is_in_sentence(rMention.arg2.extent.end, sentence.start, sentence.end)):
						print('mentionArg over sentence boundary! exit!')
					else:
						word_seg_error = preserve_relation_example(relation, rMention, out_relation_list,
						                                           sentence_index, sentence, nlp, props, word_seg_error)
	
	print('word_seg_error:{}'.format(word_seg_error))
	return out_relation_list


def get_relation_from_files(dir, outpath, sgm_dicts, doc2relations, nlp, props):
	files = glob.glob(dir + '*.sgm')
	for f in files:
		docID = os.path.splitext(os.path.basename(f))[0]
		
		relation_list = get_relations_from_file(docID, sgm_dicts, doc2relations, nlp, props)
		
		with open(outpath + docID + '.relationMention.json', 'w') as f:
			json.dump(relation_list, f, indent=4, ensure_ascii=False)


def merge_sgm_apf(sgm_dicts: Dict[str, SgmDoc], doc2entities: Dict[str, Dict[str, ApfEntity]],
                  doc2relations: Dict[str, Dict[str, ApfRelation]]) -> Dict[str, Document]:
	doc_dicts = {}
	for docID, sgm_doc in sgm_dicts.items():
		sentences = []
		for sentence_index, sgm_s in enumerate(sgm_doc.sentence_list):
			
			# entity mention
			e_dicts = {}
			e_mentions = []
			for e_id, apf_e in doc2entities[docID].items():
				entity_id = apf_e.id
				
				for apf_m in apf_e.mentions:
					char_b = apf_m.head.start
					char_e = apf_m.head.end
					if sgm_s.start <= char_b <= sgm_s.end:
						if not (sgm_s.start <= char_e <= sgm_s.end):
							print('Relation extent over sentence boundary!')
						# print(sentence['string'])
						else:
							e_mentions.append(
								EntityMention(id=apf_m.id, entity_id=entity_id, type=apf_e.type, text=apf_m.head.text,
								              char_b=char_b, char_e=char_e))
							e_dicts[apf_m.id] = EntityMention(id=apf_m.id, entity_id=entity_id, type=apf_e.type,
							                                  text=apf_m.head.text,
							                                  char_b=char_b, char_e=char_e)
			# relation mention
			r_mentions = []
			for relation_id, apf_r in doc2relations[docID].items():
				
				for apf_rm in apf_r.mentions:
					r_mention_start = apf_rm.extent.start
					r_mention_end = apf_rm.extent.end
					
					if sgm_s.start <= r_mention_start <= sgm_s.end:
						
						if not (sgm_s.start <= r_mention_end <= sgm_s.end):
							print('Relation extent over sentence boundary!')
						# print(sentence['string'])
						
						if not (is_in_sentence(apf_rm.arg1.extent.start, sgm_s.start, sgm_s.end) and
						        is_in_sentence(apf_rm.arg1.extent.end, sgm_s.start, sgm_s.end) and
						        is_in_sentence(apf_rm.arg2.extent.start, sgm_s.start, sgm_s.end) and
						        is_in_sentence(apf_rm.arg2.extent.end, sgm_s.start, sgm_s.end)):
							print('mentionArg over sentence boundary! exit!')
						else:
							
							r_mentions.append(RelationMention(id=apf_rm.id, type=apf_r.type,
							                                  arg1=e_dicts[apf_rm.arg1.id],
							                                  arg2=e_dicts[apf_rm.arg2.id]))
			
			s = Sentence(id=sentence_index, docID=docID, text=sgm_s.string, char_b=sgm_s.start, char_e=sgm_s.end,
			             entity_mentions=e_mentions, relation_mentions=r_mentions)
			sentences.append(s)
		doc_dicts[docID] = Document(id=docID, sentences=sentences)
	return doc_dicts


def parse_source(data_path):
	doc_dicts = {}
	
	for path in ['bn/', 'nw/', 'wl/']:
		fp = data_path + path + 'adj/'
		
		SgmDoc_dicts = parse_sgms(fp)
		doc2entities, doc2relations, doc2events = parse_apf_docs(fp)
		doc_dicts.update(merge_sgm_apf(SgmDoc_dicts, doc2entities, doc2relations))
	return doc_dicts


if __name__ == '__main__':
	import argparse
	
	DEBUG = 0
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', default='../Data/LDC2006T06/data/Chinese/')
	parser.add_argument('--output_path', default='./output/')
	parser.add_argument('--corenlp_path', default='http://140.109.19.190')
	
	args = parser.parse_args()
	
	data_path = args.data_path
	output_path = args.output_path
	corenlp = args.corenlp_path
	
	doc_dicts = parse_source(data_path)
	
	print(len(doc_dicts))
	print(doc_dicts["CTS20001211.1300.0012"].sentences[0].text)
	print(str(doc_dicts["CTS20001211.1300.0012"].sentences[0].char_e))

# bn_path = data_path + 'bn/adj/'
# nw_path = data_path + 'nw/adj/'
# wl_path = data_path + 'wl/adj/'

# with StanfordCoreNLP(corenlp, port=9000) as nlp:
# 	props = {'annotators': 'tokenize', 'pipelineLanguage': 'zh', 'outputFormat': 'json'}
#
# 	SgmDoc_dicts = parse_sgms(bn_path)
# 	doc2entities, doc2relations, doc2events = parse_apf_docs(bn_path)
# 	get_relation_from_files(bn_path, output_path + 'bn/adj/', SgmDoc_dicts, doc2relations, nlp, props)
#
# 	SgmDoc_dicts = parse_sgms(nw_path)
# 	doc2entities, doc2relations, doc2events = parse_apf_docs(nw_path)
# 	get_relation_from_files(nw_path, output_path + 'nw/adj/', SgmDoc_dicts, doc2relations, nlp, props)
#
# 	SgmDoc_dicts = parse_sgms(wl_path)
# 	doc2entities, doc2relations, doc2events = parse_apf_docs(wl_path)
# 	get_relation_from_files(wl_path, output_path + 'wl/adj/', SgmDoc_dicts, doc2relations, nlp, props)
