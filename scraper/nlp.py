import spacy
import json
from definitions import DATA_DIR
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
exchanges = {}

with open(f"{DATA_DIR}/dialogues.txt", encoding='utf8') as dialogues:
    for line in dialogues:
        if not line.strip():
            continue
        doc = nlp(line)
        if not doc.ents:
            continue
        speaker = doc.ents[0].text
        if speaker not in exchanges:
            exchanges[speaker] = {}
        for entity in doc.ents[1:]:
            if entity.label_ == "PERSON":
                exchanges[speaker][entity.text] = (
                    exchanges[speaker].get(entity.text, 0) + 1
                )
with open("exchanges.json", "w", encoding='utf8') as f:
    json.dump(exchanges, f, indent=4)
