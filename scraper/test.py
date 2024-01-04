import spacy
from spacy.tokens import Doc

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_trf")

# # Process whole documents
# with open('../data/gensinimpact_pages_current.xml', 'r', encoding='utf8') as f:
#     docs = nlp.pipe(f.read().split('\n\n'))

# master_doc = Doc.from_docs(docs)
# # Find named entities, phrases and concepts
# with open('ner.txt', 'w') as out:
#     for entity in master_doc.ents:
#         out.write(f"{entity.text}, {entity.label_}")

text = ":'''[[Mona]]:''' I am Astrologist Mona Megistus, meaning 'The Great Astrologist Mona.'"
doc = nlp(text)

for entity in doc.ents:
    print(entity.text, entity.label_)
