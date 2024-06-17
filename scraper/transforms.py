import spacy
import json
from definitions import DATA_DIR, XML_FILE
from tqdm import tqdm
import os
import re
import html

dialogue_pattern = re.compile(
    r"""
^:+             # Starts with one or more colons
(
    \{\{DIcon.*?\}\}.* |    # Matches {{DIcon}} followed by the rest of the text till newline
    (?:\{\{.*?\}\}\ )?      # Matches optional voice tag {{ }}
    '''[^:]+:''' .*       # Matches '''Name:''' where Name can be any characters name
)
""",
    re.VERBOSE,
)

ref_pattern = re.compile(r"<ref.*?>.*?</ref>|<ref.*?/>")
comment_pattern = re.compile(r"<!--.*?-->")
rubi_pattern = re.compile(r"{{rubi\|(.*?)\|(.*?)}}", re.IGNORECASE)
w_pattern = re.compile(r"{{w.*\|([^}]*)}}", re.IGNORECASE)
tt_pattern = re.compile(r"{{tt.*\|([^}]*)}}", re.IGNORECASE)
actor_pattern = re.compile(r".*(?:played|voiced) by (\w+ \w+|\w+)", re.IGNORECASE)
color_pattern = re.compile(r"{{color.*\|([^}]*)}}", re.IGNORECASE)
not_a_typo = re.compile(r"{{not a typo\|(.+?)}}", re.IGNORECASE)
ifeq_pattern = re.compile(r"{{#ifeq:.*\|([^}]*)}}(<!--)?", re.IGNORECASE)
mc_pattern = re.compile(r"{{mc\|((m=)?([^\|}]*))\|.*}}", re.IGNORECASE)
sic_pattern = re.compile(r"{{sic\|([^|}]+).*}}", re.IGNORECASE)
ll_pattern = re.compile(r"{{ll\|([^|}]+)\|([^|}]+)}}", re.IGNORECASE)
transclude_pattern = re.compile(r"{{Transclude.*?}}", re.IGNORECASE)
obf_pattern = re.compile(r"{{obf\|([^|}]+)}}", re.IGNORECASE)


def pick_character_dialogues_from_raw() -> int:
    """Extract all dialogue from the XML file and save it to a text file.

    Returns:
        str: The path to the saved dialogue text file.
    """

    try:
        print("Extracting dialogues from XML file...")
        with tqdm(total=os.path.getsize(f"{DATA_DIR}/{XML_FILE}")) as pbar:
            with open(f"{DATA_DIR}/{XML_FILE}", "r", encoding="utf8") as src, open(
                f"{DATA_DIR}/dialogues.txt", "w", encoding="utf8"
            ) as dst:
                line_count = 0
                for line in tqdm(src):
                    pbar.update(len(line))
                    if dialogue_pattern.match(line):
                        dst.write(clean_dialogue_line(line))
                        # dst.write(line)
                        line_count += 1
        print("Dialogue extraction complete.")

    except FileNotFoundError:
        print(f"File not found: {DATA_DIR}/{XML_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return line_count


def clean_dialogue_line(line: str) -> str:
    """Clean a line of dialogue from the XML file.

    Args:
        line (str): The line of dialogue to clean.

    Returns:
        The cleaned line of dialogue.
    """

    line = html.unescape(html.unescape(html.unescape(line)))

    # Replace DIcon with Aether
    if "{{DIcon" in line:
        start = line.find("}}") + 2
        line = f"Aether:{line[start:]}"
    else:
        line = line[line.find("'''") :]

    line = line.replace("Traveler's Sibling", "Lumine")
    line = line.replace("(Traveler)", "Aether")

    line = ref_pattern.sub(r"", line)
    line = comment_pattern.sub(r"", line)
    line = rubi_pattern.sub(r"\1 (\2)", line)
    line = w_pattern.sub(r"\1", line)
    line = color_pattern.sub(r"\1", line)
    line = not_a_typo.sub(r"\1", line)
    line = ifeq_pattern.sub(r"\1", line)
    line = mc_pattern.sub(r"\3", line)
    line = sic_pattern.sub(r"\1", line)
    line = ll_pattern.sub(r"\1\2", line)
    line = transclude_pattern.sub(r"", line)
    line = obf_pattern.sub(r"\1", line)

    def replace_tt(m):
        if actor_pattern.match(m.group(1)):
            return actor_pattern.sub(r"\1", m.group(1))
        return m.group(1)

    line = tt_pattern.sub(replace_tt, line)

    # Final cleanup
    line = line.replace("{{Dialogue End}}", "").replace("{{sic}}", "")
    line = (
        line.replace("'''", "")
        .replace("[[", "")
        .replace("]]", "")
        .replace("{{", "")
        .replace("}}", "")
    )
    return line


def count_character_exchanges_in_dialogues(line_count: int):
    # Load English tokenizer, tagger, parser and NER
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_trf")
    print("Model loaded.")
    print("Counting character exchanges in dialogues...")
    exchanges = {}
    with tqdm(total=line_count) as pbar:
        with open(f"{DATA_DIR}/dialogues.txt", encoding="utf8") as dialogues:
            for line in dialogues:
                pbar.update(1)
                if not line.strip():
                    continue
                separation_index = line.find(":")
                speaker = line[:separation_index]
                if speaker not in exchanges:
                    exchanges[speaker] = {}
                doc = nlp(line[separation_index + 1 :])
                if not doc.ents:
                    continue
                for entity in doc.ents:
                    if entity.label_ == "PERSON":
                        if entity.text not in exchanges[speaker]:
                            exchanges[speaker][entity.text] = 1
                        else:
                            exchanges[speaker][entity.text] += 1
    with open(f"{DATA_DIR}/exchanges.json", "w", encoding="utf8") as f:
        print("Dumping exchanges to JSON file...")
        json.dump(exchanges, f, indent=4)
        print("Exchanges counted and saved to exchanges.json.")


def find_all_tags():
    pattern = re.compile(r"{{.*?}}")
    unique_tags = set()
    with open(f"{DATA_DIR}/dialogues.txt", encoding="utf8") as dialogues:
        for line in dialogues:
            tags = pattern.findall(line)
            for tag in tags:
                unique_tags.add(tag)
    with open("tags.txt", "w", encoding="utf8") as f:
        for tag in unique_tags:
            f.write(f"{tag}\n")
    print(unique_tags)


if __name__ == "__main__":
    line_count = pick_character_dialogues_from_raw()
    count_character_exchanges_in_dialogues(line_count)
